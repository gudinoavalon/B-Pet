import json
import logging
import time
import threading
import os
from bambu_mqtt import BambuMqttClient
from display import EpaperDisplay
from ui import draw_ui
from pet import Pet
from web_server import run_web

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

state = {
    "connected": False,
    "gcode_state": "UNKNOWN",
    "wifi_signal": 0
}

pet = Pet()

def load_config():
    if not os.path.exists("config.json"):
        return {}
    with open("config.json", "r") as f:
        return json.load(f)

def run():
    config = load_config()
    printer_ip = config.get("printer", {}).get("ip", "")
    printer_serial = config.get("printer", {}).get("serial", "")
    printer_code = config.get("printer", {}).get("access_code", "")
    
    # Run Flask Web Server in background thread
    web_port = config.get("web", {}).get("port", 8080)
    logger.info(f"Starting web configuration interface on port {web_port}")
    web_thread = threading.Thread(target=run_web, args=(web_port,), daemon=True)
    web_thread.start()
    
    # Intialize MQTT tracking
    mqtt_client = None
    if printer_ip and printer_serial and printer_code:
        mqtt_client = BambuMqttClient(printer_ip, printer_serial, printer_code, state)
        mqtt_client.connect()
    else:
        logger.warning("Printer details not fully configured. Please use Web UI via http://<PI_IP>:8080/")
        pet.face = "(?_?)"
        pet.status = "No Config"
        
    # Setup Display
    display = EpaperDisplay()
    has_display = display.init()
    if not has_display:
        logger.info("Will render UI locally to debug_ui.png without pushing to e-Paper.")
    
    try:
        while True:
            pet.update(state)
            
            # Generates a PIL Image (250x122 monochrome)
            img = draw_ui(state, pet)
            
            # Dump to PNG for local verification/debugging
            img.save("debug_ui.png")
            
            if has_display:
                display.update(img)
                
            time.sleep(5) # Update screen every 5 seconds to throttle e-paper wear/battery
            
    except KeyboardInterrupt:
        logger.info("Got termination signal, shutting down...")
    finally:
        if mqtt_client:
            mqtt_client.disconnect()
        if has_display:
            display.close()

if __name__ == "__main__":
    run()

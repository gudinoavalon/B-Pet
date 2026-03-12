import ssl
import json
import logging
import time
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class BambuMqttClient:
    def __init__(self, ip, serial, access_code, state_dict):
        self.ip = ip
        self.serial = serial
        self.access_code = access_code
        self.state = state_dict
        
        self.state["connected"] = False
        
        self.client = mqtt.Client(client_id=f"bambu_pet_{int(time.time())}")
        self.client.username_pw_set("bblp", self.access_code)
        
        # Disable cert verification since Bambu uses self-signed
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        
    def connect(self):
        try:
            logger.info(f"Connecting to Bambu Printer at {self.ip}...")
            self.client.connect(self.ip, 8883, 60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT Connect failed: {e}")
            self.state["connected"] = False
            
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        
    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info("Connected to Bambu Printer!")
            self.state["connected"] = True
            topic = f"device/{self.serial}/report"
            self.client.subscribe(topic)
            self.request_pushall()
        else:
            logger.warning(f"Connection failed with code {rc}")
            self.state["connected"] = False
            
    def on_disconnect(self, client, userdata, rc, properties=None):
        logger.info(f"Disconnected from Bambu Printer. rc={rc}")
        self.state["connected"] = False

    def request_pushall(self):
        topic = f"device/{self.serial}/request"
        payload = {
            "pushing": {
                "sequence_id": str(int(time.time())),
                "command": "pushall"
            }
        }
        self.client.publish(topic, json.dumps(payload))

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            if "print" in data:
                print_data = data["print"]
                
                # Delta update
                keys = [
                    "gcode_state", "mc_percent", "mc_remaining_time",
                    "nozzle_temper", "nozzle_target_temper",
                    "bed_temper", "bed_target_temper",
                    "cooling_fan_speed", "wifi_signal"
                ]
                
                for k in keys:
                    if k in print_data:
                        self.state[k] = print_data[k]
                        
                # Fix fan speed (0-15 scale to 0-100)
                if "cooling_fan_speed" in print_data:
                    fan_val = float(print_data["cooling_fan_speed"])
                    self.state["cooling_fan_speed"] = int((fan_val / 15.0) * 100)
                    
        except json.JSONDecodeError:
            pass

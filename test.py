from ui import draw_ui
from pet import Pet

def test_render():
    p = Pet()
    # Dummy printing state
    state = {
        "connected": True,
        "gcode_state": "RUNNING",
        "nozzle_temper": 220,
        "nozzle_target_temper": 220,
        "bed_temper": 60,
        "bed_target_temper": 60,
        "cooling_fan_speed": 75,
        "mc_percent": 42,
        "mc_remaining_time": 125,
        "wifi_signal": -40
    }
    p.update(state)
    img = draw_ui(state, p)
    img.save("test_ui_printing.png")
    print("Test image generated successfully: test_ui_printing.png")
    
if __name__ == "__main__":
    test_render()

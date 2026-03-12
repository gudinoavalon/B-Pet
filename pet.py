class Pet:
    def __init__(self):
        self.face = "(>_>)"
        self.status = "Idle"

    def update(self, state):
        gcode_state = state.get("gcode_state", "UNKNOWN")
        temp = state.get("nozzle_temper", 0)
        connected = state.get("connected", False)
        percent = state.get("mc_percent", 0)
        
        if not connected:
            self.face = "(x_x)"
            self.status = "Offline"
        elif gcode_state == "RUNNING":
            if percent < 10:
                self.face = "(ò_ó)"    # Focused to start
            elif percent > 90:
                self.face = "(^o^)"    # Almost there!
            else:
                self.face = "(o_o)"    # Watching attentively
            self.status = "Printing"
        elif gcode_state == "FINISH":
            self.face = "(^w^)"
            self.status = "Done!"
        elif temp > 50:
            self.face = "(~_~)"        # Hot
            self.status = "Cooling"
        else:
            self.face = "(-_-)zzz"     # Idle for a while
            self.status = "Zzz..."

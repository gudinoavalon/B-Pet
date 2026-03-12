import os
import json
import time

STATS_FILE = "stats.json"

class Pet:
    def __init__(self):
        self.face = "(>_>)"
        self.status = "Idle"
        
        # Leveling System
        self.total_print_seconds = 0
        self.level = 1
        self.last_update_time = time.time()
        self.load_stats()

    def load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    data = json.load(f)
                    self.total_print_seconds = data.get("total_print_seconds", 0)
                    self.update_level()
            except Exception:
                pass

    def save_stats(self):
        with open(STATS_FILE, "w") as f:
            json.dump({"total_print_seconds": self.total_print_seconds}, f)

    def update_level(self):
        # Level calculation: 1 hour = ~Lvl 2, 10 hours = ~Lvl 6, 100 hours = ~Lvl 20
        hours = self.total_print_seconds / 3600.0
        # Simple curve: Lvl = int(sqrt(hours) * 2) + 1
        self.level = int((hours ** 0.5) * 2) + 1

    def update(self, state):
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now
        
        gcode_state = state.get("gcode_state", "UNKNOWN")
        temp = state.get("nozzle_temper", 0)
        connected = state.get("connected", False)
        percent = state.get("mc_percent", 0)
        
        if gcode_state == "RUNNING":
            self.total_print_seconds += dt
            self.update_level()
            
            # Save every ~5 minutes of printing to reduce SD card writes
            if int(self.total_print_seconds) % 300 < int(dt):
                self.save_stats()
        
        if not connected:
            self.face = "[x_x]" # Dead Extruder
            self.status = "Offline"
        elif gcode_state == "RUNNING":
            if percent < 10:
                self.face = "[ò_ó]"    # Concentrating nozzle
            elif percent > 90:
                self.face = "[^o^]"    # Happy nozzle
            else:
                self.face = "[o_o]"    # Extruding
            self.status = "Printing"
        elif gcode_state == "FINISH":
            self.face = "[^w^]"
            self.status = "Done!"
        elif temp > 50:
            self.face = "[~_~]"        # Hot nozzle
            self.status = "Cooling"
        else:
            self.face = "[-_-]z"     # Sleeping nozzle
            self.status = "Zzz..."

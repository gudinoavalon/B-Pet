import logging
from PIL import Image

logger = logging.getLogger(__name__)

class EpaperDisplay:
    def __init__(self):
        self.epd = None
        self.initialized = False
        try:
            from waveshare_epd import epd2in13_V4
            self.epd = epd2in13_V4.EPD()
        except ImportError:
            logger.error("waveshare_epd not found. Will simulate display output locally.")
            
    def init(self):
        if not self.epd:
            return False
            
        try:
            logger.info("Initializing e-Paper...")
            self.epd.init()
            # Clear screen once on boot to prevent ghosting
            self.epd.Clear(0xFF)
            self.initialized = True
            return True
        except Exception as e:
            logger.error(f"Failed to initialize e-Paper: {e}")
            return False
            
    def update(self, image):
        if not self.initialized or not self.epd:
            return
            
        try:
            # Re-init for a full refresh
            self.epd.init()
            self.epd.display(self.epd.getbuffer(image))
            self.epd.sleep()
        except Exception as e:
            logger.error(f"Failed to update e-Paper: {e}")
            
    def close(self):
        if self.initialized and self.epd:
            self.epd.sleep()
            try:
                self.epd.Dev_exit()
            except:
                pass

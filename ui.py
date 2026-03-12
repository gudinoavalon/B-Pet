from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 250
HEIGHT = 122

def get_font(size):
    # Try common Raspbian fonts
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    for font_path in fonts:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

def draw_ui(state, pet):
    img = Image.new('1', (WIDTH, HEIGHT), 255) # White background
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(32)
    font_medium = get_font(16)
    font_small = get_font(12)
    
    # Top Bar (Inverted)
    draw.rectangle((0, 0, WIDTH, 18), fill=0)
    draw.text((4, 2), "B-Pet", font=font_small, fill=255)
    
    # Status on right side of top bar
    # Using small font
    status_text = pet.status
    if state.get("connected"):
        status_text += f" | {state.get('wifi_signal', '-')}dBm"
    draw.text((WIDTH - 80, 2), status_text, font=font_small, fill=255)
    
    # Main Pet Face
    draw.text((10, 40), pet.face, font=font_large, fill=0)
    
    # Stats Region
    nozzle = state.get("nozzle_temper", 0)
    nozzle_target = state.get("nozzle_target_temper", 0)
    bed = state.get("bed_temper", 0)
    bed_target = state.get("bed_target_temper", 0)
    
    draw.text((130, 25), f"NZL:{nozzle}/{nozzle_target}°C", font=font_medium, fill=0)
    draw.text((130, 45), f"BED:{bed}/{bed_target}°C", font=font_medium, fill=0)
    
    # Fan speeds
    fan = state.get("cooling_fan_speed", 0)
    draw.text((130, 65), f"FAN:{fan}%", font=font_medium, fill=0)
    
    # Progress Bar
    progress = state.get("mc_percent", 0)
    time_left = state.get("mc_remaining_time", 0)
    
    bar_x = 10
    bar_y = 95
    bar_w = WIDTH - 20
    bar_h = 18
    
    draw.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), outline=0)
    
    inner_w = int((progress / 100.0) * (bar_w - 4))
    if inner_w > 0:
        draw.rectangle((bar_x + 2, bar_y + 2, bar_x + 2 + inner_w, bar_y + bar_h - 2), fill=0)
        
    prog_text = f"{progress}%"
    if time_left > 0:
        prog_text += f" - {time_left}m left"
        
    # Draw text inside or outside progress bar depending on width
    if inner_w > (bar_w / 2):
        draw.text((bar_x + 10, bar_y + 2), prog_text, font=font_small, fill=255)
    else:
        draw.text((bar_x + inner_w + 5, bar_y + 2), prog_text, font=font_small, fill=0)
        
    return img

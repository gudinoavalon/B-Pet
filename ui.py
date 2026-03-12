from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

WIDTH = 250
HEIGHT = 122

def get_font(size):
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
    font_medium = get_font(14)
    font_small = get_font(12)
    
    # --- Top Bar (Inverted) ---
    draw.rectangle((0, 0, WIDTH, 16), fill=0)
    
    # Left: Name & Level
    draw.text((4, 1), f"B-Pet | Lvl {pet.level}", font=font_small, fill=255)
    
    # Right: Clock & Status
    clock_str = datetime.now().strftime("%H:%M")
    right_text = f"{pet.status} | {clock_str}"
    if state.get("connected"):
        right_text = f"{state.get('wifi_signal', '-')}dBm | " + right_text
        
    # Estimate text width (rough, as textlength is best but varies by PIL version)
    # Using anchor='ra' for right alignment if supported, or manually inset
    try:
        w = draw.textlength(right_text, font=font_small)
        draw.text((WIDTH - w - 4, 1), right_text, font=font_small, fill=255)
    except AttributeError:
        draw.text((WIDTH - 120, 1), right_text, font=font_small, fill=255)
        
    # --- The Pet Face (Left Side) ---
    # Draw a mock 3D printer hotend casing around the text face
    hx, hy = 5, 25
    hw, hh = 120, 65
    
    # Draw hotend box
    draw.rectangle((hx, hy, hx+hw, hy+hh), outline=0, width=2)
    # Draw nozzle tip
    draw.polygon([(hx+hw//2 - 10, hy+hh), (hx+hw//2 + 10, hy+hh), (hx+hw//2, hy+hh+15)], fill=0)
    
    # Center face in hotend
    try:
        fw = draw.textlength(pet.face, font=font_large)
        draw.text((hx + (hw - fw)//2, hy + 10), pet.face, font=font_large, fill=0)
    except AttributeError:
        draw.text((hx + 10, hy + 10), pet.face, font=font_large, fill=0)
        
    # Total Hours below Hotend
    hrs = round(pet.total_print_seconds / 3600.0, 1)
    draw.text((hx + 5, hy+hh + 4), f"Tot: {hrs}h", font=font_small, fill=0)
    
    # --- Stats Region (Right Side) ---
    sx = 135
    sy = 25
    nozzle = state.get("nozzle_temper", 0)
    nozzle_target = state.get("nozzle_target_temper", 0)
    bed = state.get("bed_temper", 0)
    bed_target = state.get("bed_target_temper", 0)
    fan = state.get("cooling_fan_speed", 0)
    
    draw.text((sx, sy), f"N: {nozzle}/{nozzle_target}°C", font=font_medium, fill=0)
    draw.text((sx, sy + 20), f"B: {bed}/{bed_target}°C", font=font_medium, fill=0)
    draw.text((sx, sy + 40), f"F: {fan}%", font=font_medium, fill=0)
    
    # --- Progress Bar (Bottom) ---
    progress = state.get("mc_percent", 0)
    time_left = state.get("mc_remaining_time", 0)
    
    bar_x = 135
    bar_y = 90
    bar_w = WIDTH - bar_x - 5
    bar_h = 20
    
    draw.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), outline=0, width=2)
    
    inner_w = int((progress / 100.0) * (bar_w - 4))
    if inner_w > 0:
        draw.rectangle((bar_x + 2, bar_y + 2, bar_x + 2 + inner_w, bar_y + bar_h - 2), fill=0)
        
    prog_text = f"{progress}%"
    if time_left > 0 and progress < 100:
        prog_text += f" ({time_left}m)"
        
    # Draw text inside or outside progress bar depending on width
    if inner_w > (bar_w / 2):
        draw.text((bar_x + 5, bar_y + 3), prog_text, font=font_small, fill=255)
    else:
        draw.text((bar_x + inner_w + 5, bar_y + 3), prog_text, font=font_small, fill=0)
        
    return img

# B-Pet (Bambu Pet)

A virtual pet and dashboard for your Bambu Lab 3D Printer, built for the Raspberry Pi Zero W with a Waveshare 2.13" Black/White e-Paper Display (Pwnagotchi hardware).

B-Pet connects to your printer via local MQTT (TLS) to monitor temperatures, progress, and print state. The virtual pet will react and change its face depending on what the printer is doing!

## Hardware Requirements
- Raspberry Pi Zero W or Zero 2 W
- Waveshare 2.13inch e-Paper HAT (Rev2.1 or V4)
- Micro SD Card
- Power Supply

## Installation on Raspberry Pi

1. Flash Raspberry Pi OS Lite (Legacy or Bookworm)
2. Enable SPI in `raspi-config`
3. Clone this repository
4. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-pil python3-rpi.gpio python3-spidev
   ```
5. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt 
   ```

## Configuration

B-Pet includes a built-in web configuration portal!
1. Start the application:
   ```bash
   python3 main.py
   ```
2. Open a web browser to `http://<YOUR_PI_IP>:8080/`
3. Enter your Bambu Lab Printer IP, Serial Number, and LAN Access Code (found in the printer's network settings).
4. Click "Save & Restart"

*Alternatively, manually edit `config.json`.*

## Running as a Service

To run B-Pet automatically on boot, create a systemd service:

```ini
[Unit]
Description=Bambu Pet Dashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/BambuHelper
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## Features

- **Pet Expressions**: 
  - `(>_>)` Idle
  - `(-_-)zzz` Sleeping (printer inactive)
  - `(ò_ó)` Printing (focused)
  - `(^o^)` Almost done
  - `(^w^)` Finished print
  - `(~_~)` Cooling down
  - `(x_x)` Offline / Disconnected
- **Dashboard Stats**: Nozzle/Bed temp, Target temp, Fan speed, Print Progress, Time Remaining.
- **Web UI**: Easy web-based configuration.
- **E-Paper Optimized**: Optimized layout for 250x122 monochrome displays. Local PNG debugging if no screen is attached.

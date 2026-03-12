# B-Pet (Bambu Pet)

A virtual pet and dashboard for your Bambu Lab 3D Printer, built for the Raspberry Pi Zero W with a Waveshare 2.13" Black/White e-Paper Display (Pwnagotchi hardware).

B-Pet connects to your printer via local MQTT (TLS) to monitor temperatures, progress, and print state. The virtual pet will react and change its face depending on what the printer is doing!

## Hardware Requirements
- Raspberry Pi Zero W or Zero 2 W
- Waveshare 2.13inch e-Paper HAT (Rev2.1 or V4)
- Micro SD Card
- Power Supply

## Installation on Raspberry Pi (1-Click)

The easiest way to install B-Pet is using the automated 1-Click Installer!

1. Flash Raspberry Pi OS Lite (Bookworm or Legacy) to your SD card.
2. Connect to Wi-Fi and SSH into your Pi.
3. Clone this repository:
   ```bash
   git clone https://github.com/gudinoavalon/B-Pet.git
   cd B-Pet
   ```
4. Run the installer script:
   ```bash
   sudo ./install.sh
   ```

The script will automatically install system dependencies, setup the Python virtual environment, enable the SPI interface, and register `b-pet.service` to start securely on boot!

## Manual Configuration / Web UI

B-Pet includes a built-in web configuration portal.

If you used the 1-Click Installer, the app is already running! Simply:
1. Open a web browser to `http://<YOUR_PI_IP>:8080/`
2. Enter your Bambu Lab Printer IP, Serial Number, and LAN Access Code (found in the printer's network settings).
3. Click "Save & Restart"

*Alternatively, manually edit `config.json` in the root folder and restart the service.*

## Features

- **Pet Expressions**: 
  - `[>_>]` Idle
  - `[-_-]z` Sleeping (printer inactive)
  - `[ò_ó]` Printing (focused)
  - `[^o^]` Almost done
  - `[^w^]` Finished print
  - `[~_~]` Cooling down
  - `[x_x]` Offline / Disconnected
- **Leveling System**: The Pet tracks the total hours your printer runs and automatically levels up over time! You can track "Total Print Hours" beneath the extruder graphic.
- **Dashboard Stats**: Nozzle/Bed temp, Target temp, Fan speed, Print Progress, and Time Remaining.
- **Web UI (Port 8080)**: Easy web-based configuration and stats dashboard.
- **E-Paper Optimized**: Optimized layout for 250x122 monochrome Waveshare displays.

#!/bin/bash

# B-Pet 1-Click Installer for Raspberry Pi
echo "======================================"
echo "    B-Pet 1-Click Installer         "
echo "======================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

echo "1. Updating APT packages..."
apt-get update

echo "2. Installing required system packages for SPI and Pillow..."
apt-get install -y python3-pip python3-pil python3-rpi.gpio python3-spidev python3-venv git

echo "3. Creating Python virtual environment (if needed by Bookworm)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "4. Installing Python dependencies..."
./venv/bin/pip install -r requirements.txt

echo "5. Enabling SPI interface via raspi-config..."
if command -v raspi-config > /dev/null; then
  # raspi-config nonint do_spi 0 -> turns it ON
  raspi-config nonint do_spi 0
  echo "SPI enabled."
else
  echo "Warning: raspi-config not found. Make sure SPI is enabled in your OS!"
fi

echo "6. Establishing Systemd Service..."
SERVICE_PATH="/etc/systemd/system/b-pet.service"
CURRENT_DIR=$(pwd)
USER_NAME=$(cat /etc/passwd | grep 1000 | cut -d: -f1 | head -n 1)

if [ -z "$USER_NAME" ]; then
    USER_NAME="pi"
fi

cat > $SERVICE_PATH << EOL
[Unit]
Description=B-Pet Bambu Dashboard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

echo "Reloading systemd daemon..."
systemctl daemon-reload
echo "Enabling b-pet.service on boot..."
systemctl enable b-pet.service
echo "Starting b-pet.service now..."
systemctl start b-pet.service

echo "======================================"
echo " Installation Complete!               "
echo " B-Pet is now running in the background."
echo " Configure your printer via Web UI:   "
echo " http://$(hostname -I | awk '{print $1}'):8080/ "
echo "======================================"

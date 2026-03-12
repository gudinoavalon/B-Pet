import json
import os
import logging
from flask import Flask, render_template_string, request

app = Flask(__name__)
# Suppress flask verbose logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

CONFIG_PATH = "config.json"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>B-Pet Config</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: monospace; background: #222; color: #fff; padding: 20px; max-width: 600px; margin: auto; }
        .group { background: #333; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #aaa; }
        input[type=text], input[type=password] { background: #111; color: #fff; border: 1px solid #555; padding: 10px; width: 100%; box-sizing: border-box; margin-bottom: 15px; border-radius: 4px; }
        input[type=submit] { background: #4caf50; color: white; border: none; padding: 12px 20px; cursor: pointer; border-radius: 4px; font-weight: bold; width: 100%; font-size: 16px; }
        input[type=submit]:hover { background: #45a049; }
        h1 { border-bottom: 2px solid #555; padding-bottom: 10px; }
    </style>
</head>
<body>
    <h1>(>_>) B-Pet Config</h1>
    <div class="group">
        <form method="POST">
            <label>Printer IP Address:</label>
            <input type="text" name="ip" value="{{ config.printer.ip }}" placeholder="192.168.1.100">
            
            <label>Printer Serial Number:</label>
            <input type="text" name="serial" value="{{ config.printer.serial }}" placeholder="00M00A...">
            
            <label>LAN Access Code:</label>
            <input type="password" name="access_code" value="{{ config.printer.access_code }}" placeholder="8 characters">
            
            <input type="submit" value="Save & Restart Application">
        </form>
    </div>
</body>
</html>
"""

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(conf):
    with open(CONFIG_PATH, "w") as f:
        json.dump(conf, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    conf = load_config()
    if request.method == "POST":
        if "printer" not in conf:
            conf["printer"] = {}
        conf["printer"]["ip"] = request.form.get("ip", "")
        conf["printer"]["serial"] = request.form.get("serial", "")
        conf["printer"]["access_code"] = request.form.get("access_code", "")
        save_config(conf)
        # Terminate to allow systemd to restart and apply new config
        os._exit(1) 
    return render_template_string(HTML_TEMPLATE, config=conf)

def run_web(port=8080):
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

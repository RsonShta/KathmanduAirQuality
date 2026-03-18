"""
main.py
Sends simulated air quality data to ThingsBoard using MQTT.

- Reads config file
- Connects to ThingsBoard
- Sends data every few seconds
- Logs data and warnings
"""

import json
import time
import logging
import paho.mqtt.client as mqtt
from sensor_sim import get_reading


# Load configuration from config.json
with open("config.json") as f:
    cfg = json.load(f)

HOST     = cfg["thingsboard_host"]
TOKEN    = cfg["access_token"]
CLIENT   = cfg["client_id"]
INTERVAL = cfg.get("telemetry_interval")
SAFE     = cfg.get("safe_values", {})


# Setup logging (save logs + show in console)
logging.basicConfig(
    filename="logs/aq_sensor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger()
log.addHandler(logging.StreamHandler())


# Setup MQTT client
client = mqtt.Client(client_id=CLIENT)
client.username_pw_set(TOKEN)


# Called when connection is established
def on_connect(c, u, f, rc):
    if rc == 0:
        log.info("Connected to ThingsBoard")
    else:
        log.error("Connection failed rc=%d", rc)

client.on_connect = on_connect


# Connect to ThingsBoard server
client.connect(HOST, 1883, 60)
client.loop_start()

log.info("Station started | Host=%s | Interval=%ds", HOST, INTERVAL)


# Main loop (runs continuously)
try:
    while True:
        # Get simulated data
        data = get_reading()

        # Send data to ThingsBoard
        client.publish("v1/devices/me/telemetry", json.dumps(data), qos=1)

        # Show data in console/log
        peak = "[PEAK]" if data["peak_hour"] else "      "

        log.info(
            "%s PM2.5=%-5.1f PM10=%-5.1f NO2=%-4.1f CO2=%-5.0f "
            "T=%.1f°C H=%.1f%% | AQI=%d",
            peak, data["pm25"], data["pm10"], data["no2"], data["co2"],
            data["temperature"], data["humidity"],
            data["aqi"],
        )

        # Check safe limits and show warnings
        for key, limit in SAFE.items():
            value = data.get(key)

            if value is not None and value > limit:
                log.warning(
                    "ALERT: %s = %.1f exceeded safe limit %.1f",
                    key, value, limit
                )

        # Wait before next reading
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    log.info("Stopped by user")

finally:
    client.loop_stop()
    client.disconnect()
    log.info("Disconnected from server")
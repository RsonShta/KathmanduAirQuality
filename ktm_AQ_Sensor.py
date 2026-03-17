import json
import time
import logging
import paho.mqtt.client as mqtt
from datetime import datetime
from modules.sensor_sim import get_kathmandu_data

# ----------------------
# Load Config
# ----------------------
with open("config.json") as f:
    config = json.load(f)

THINGSBOARD_HOST = config["thingsboard_host"]
ACCESS_TOKEN = config["access_token"]
CLIENT_ID = config["client_id"]
INTERVAL = config.get("telemetry_interval", 10)  # default to 10s if not set

# ----------------------
# Setup Logging
# ----------------------
logging.basicConfig(
    filename="logs/aq_sensor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ----------------------
# MQTT Callbacks
# ----------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[SUCCESS] Connected to ThingsBoard Cloud")
        logging.info("Connected to ThingsBoard Cloud")
    else:
        print(f"[ERROR] Connection failed with code {rc}")
        logging.error(f"Connection failed with code {rc}")

# ----------------------
# Initialize MQTT Client
# ----------------------
client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.username_pw_set(ACCESS_TOKEN)

try:
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()

    print("Starting Kathmandu Air Quality Station...")
    print("-------------------------------------------")

    while True:
        # Generate telemetry data
        data = get_kathmandu_data()  # make sure it returns 'no2' as well

        # Logging output
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = (
            f"[{timestamp}] Data Sent: PM2.5: {data['pm25']} µg/m³ | "
            f"PM10: {data['pm10']} µg/m³ | NO2: {data['no2']} µg/m³ | "
            f"CO2: {data['co2']} ppm | Temp: {data['temperature']}°C | "
            f"Humidity: {data['humidity']}%"
        )

        print(log_msg)
        logging.info(log_msg)

        # Publish telemetry to ThingsBoard
        client.publish("v1/devices/me/telemetry", json.dumps(data), qos=1)

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nSimulation stopped by user.")
    logging.info("Simulation stopped by user.")

finally:
    client.loop_stop()
    client.disconnect()
    print("Disconnected safely.")
    logging.info("Disconnected safely.")
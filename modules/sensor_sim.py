import random
from datetime import datetime

# Configuration for easy adjustment
TEMP_START = 22.0
TEMP_MIN = 18.0
TEMP_MAX = 26.0
TEMP_DELTA = 0.2

HUM_START = 55.0
HUM_MIN = 0
HUM_MAX = 100
HUM_DELTA = 0.5

BASE_PM25 = 60.0
BASE_CO2 = 500.0
BASE_NO2 = 30.0

def get_kathmandu_data():
    """
    Simulates Kathmandu air quality telemetry data realistically.
    Traffic peaks: 7-10 AM, 3-7 PM.
    Returns dictionary: pm25, pm10, co2, no2, temperature, humidity.
    """
    hour = datetime.now().hour

    # --- PM2.5 & PM10 --- #
    # Rush hour multiplier
    if 7 <= hour <= 13 or 16 <= hour <= 19:
        pm_multiplier = random.uniform(1.5, 2.5)
    else:
        pm_multiplier = random.uniform(0.8, 1.2)

    pm25 = round(BASE_PM25 * pm_multiplier + random.uniform(-5, 5), 2)
    pm10 = round(pm25 * 1.4 + random.uniform(-3, 3), 2)

    # --- CO2 --- #
    # Slightly higher during traffic hours
    if 7 <= hour <= 13 or 16 <= hour <= 19:
        co2 = round(BASE_CO2 + random.uniform(50, 200), 1)
    else:
        co2 = round(BASE_CO2 + random.uniform(-50, 50), 1)

    # --- NO2 --- #
    # Correlates with PM2.5
    no2 = round(BASE_NO2 + (pm25 - BASE_PM25) * 0.5 + random.uniform(-5, 5), 1)

    # --- Temperature (gradual change) --- #
    if not hasattr(get_kathmandu_data, "prev_temp"):
        get_kathmandu_data.prev_temp = TEMP_START
    delta_temp = random.uniform(-TEMP_DELTA, TEMP_DELTA)
    get_kathmandu_data.prev_temp += delta_temp
    get_kathmandu_data.prev_temp = max(TEMP_MIN, min(TEMP_MAX, get_kathmandu_data.prev_temp))
    temperature = round(get_kathmandu_data.prev_temp, 1)

    # --- Humidity (gradual change inversely related to temperature) --- #
    if not hasattr(get_kathmandu_data, "prev_hum"):
        get_kathmandu_data.prev_hum = HUM_START
    delta_hum = random.uniform(-HUM_DELTA, HUM_DELTA)
    # slight inverse relation: higher temp, slightly lower humidity
    delta_hum -= (get_kathmandu_data.prev_temp - TEMP_START) * 0.1
    get_kathmandu_data.prev_hum += delta_hum
    get_kathmandu_data.prev_hum = max(HUM_MIN, min(HUM_MAX, get_kathmandu_data.prev_hum))
    humidity = round(get_kathmandu_data.prev_hum, 1)

    return {
        "pm25": pm25,
        "pm10": pm10,
        "co2": co2,
        "no2": no2,
        "temperature": temperature,
        "humidity": humidity,
        "location": "Kathmandu_Station_01"
    }
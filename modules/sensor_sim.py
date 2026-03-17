import random
from datetime import datetime

def get_kathmandu_data():
    """
    Simulates Kathmandu air quality telemetry data.
    Traffic peaks: 7-10 AM, 3-7 PM
    Returns a dictionary with PM2.5, PM10, CO2, NO2, temp, humidity.
    """
    hour = datetime.now().hour
    
    # Base PM2.5
    base_pm25 = 60.0
    
    # Simulate rush hour
    if (7 <= hour <= 10) or (16 <= hour <= 19):
        peak_multiplier = random.uniform(1.5, 3.0)  # high pollution
    else:
        peak_multiplier = random.uniform(0.8, 1.2)  # normal
    
    pm25 = round(base_pm25 * peak_multiplier, 2)
    pm10 = round(pm25 * 1.4, 2)
    co2 = round(random.uniform(400, 1000), 1)
    no2 = round(random.uniform(20, 120), 1)
    temperature = round(random.uniform(18, 26), 1)
    humidity = round(random.uniform(45, 65), 1)
    
    return {
        "pm25": pm25,
        "pm10": pm10,
        "co2": co2,
        "no2": no2,
        "temperature": temperature,
        "humidity": humidity,
        "location": "Kathmandu_Station_01"
    }
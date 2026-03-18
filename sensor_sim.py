"""
sensor_sim.py
Simulates air quality data for Kathmandu.

- Generates pollutant values (PM2.5, PM10, NO2, CO2)
- Simulates temperature and humidity changes
- Calculates ONLY the final AQI value (no sub AQI shown)
"""

import random
from datetime import datetime

# Store previous temperature and humidity so they change gradually (not jump randomly)
_temp = 22.0
_hum  = 55.0


# AQI breakpoint tables
# Each tuple = (concentration_low, concentration_high, aqi_low, aqi_high)
PM25_BP = [(0,12,0,50),(12.1,35.4,51,100),(35.5,55.4,101,150),
           (55.5,150.4,151,200),(150.5,250.4,201,300),(250.5,500.4,301,500)]

PM10_BP = [(0,54,0,50),(55,154,51,100),(155,254,101,150),
           (255,354,151,200),(355,424,201,300),(425,604,301,500)]

NO2_BP  = [(0,53,0,50),(54,100,51,100),(101,360,101,150),
           (361,649,151,200),(650,1249,201,300),(1250,2049,301,500)]

CO2_BP  = [(0,400,0,50),(401,600,51,100),(601,800,101,150),
           (801,1000,151,200),(1001,1500,201,300),(1501,5000,301,500)]


def _sub_aqi(concentration, breakpoints):
    """
    Convert pollutant concentration to AQI using breakpoint table.
    This is required because AQI is calculated from pollutant values.
    """
    for lo, hi, aqi_lo, aqi_hi in breakpoints:
        if lo <= concentration <= hi:
            # Linear formula used in AQI calculation
            return round(((aqi_hi - aqi_lo) / (hi - lo)) * (concentration - lo) + aqi_lo)

    return 500  # If value is too high, return max AQI


def get_reading():
    """
    Generate one set of sensor readings.
    Returns raw data + final AQI value.
    """

    global _temp, _hum

    # Get current hour to simulate traffic pollution
    hour = datetime.now().hour

    # Peak hours (more pollution)
    peak = (7 <= hour <= 10) or (15 <= hour <= 19)

    # Increase pollution during peak hours
    multiplier = random.uniform(1.5, 2.5) if peak else random.uniform(0.8, 1.2)

    # Generate pollutant values
    pm25 = round(60.0 * multiplier + random.uniform(-5, 5), 2)
    pm10 = round(pm25 * 1.4 + random.uniform(-3, 3), 2)
    no2  = round(max(0, 30.0 + (pm25 - 60.0) * 0.5 + random.uniform(-5, 5)), 1)
    co2  = round(500.0 + (random.uniform(50, 200) if peak else random.uniform(-50, 50)), 1)

    # Slowly adjust temperature and humidity (realistic change)
    _temp = round(max(18.0, min(26.0, _temp + random.uniform(-0.2, 0.2))), 1)
    _hum  = round(max(30.0, min(95.0, _hum  + random.uniform(-0.5, 0.5))), 1)

    # Calculate AQI (take highest among pollutants)
    aqi = max([
        _sub_aqi(pm25, PM25_BP),
        _sub_aqi(pm10, PM10_BP),
        _sub_aqi(no2,  NO2_BP),
        _sub_aqi(co2,  CO2_BP)
    ])

    return {
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "co2": co2,
        "temperature": _temp,
        "humidity": _hum,
        "aqi": aqi,
        "location": "Kathmandu_Station_01",
        "peak_hour": peak,
    }
{
"pm25": 100,
"pm10": 150,
"co2": 800,
"no2": 80
->>These are the values claimed as safe or normal. We can change these values from config.json directly as per the requirement.
}

Situation.
The Kathmandu Air Quality Station simulates sensor readings, showing higher pollution during traffic peak hours (7–10 AM & 3–7 PM) and normal levels at other times. Telemetry for PM2.5, PM10, CO2, and NO2 is sent to ThingsBoard, where alarms trigger automatically when thresholds are exceeded.

Architecture:
The system consists of a Python-based sensor simulation that generates real-time air quality telemetry for Kathmandu and publishes it to ThingsBoard Cloud via MQTT. ThingsBoard manages data storage, evaluates thresholds through TBEL-based alarm rules, and provides real-time visualization and alerting on dashboards


-------This project simulates air quality data for Kathmandu and sends it to ThingsBoard using MQTT. It is structured as a modular Python system for testing and experimentation.-------------
-------All key settings, including ThingsBoard host, access token, and device information, are stored in config.json, keeping configuration separate from the code.---------
-------The main Python script handles the core tasks of connecting to MQTT, generating telemetry data, and sending it to ThingsBoard at regular intervals.--------------
-------Supporting scripts are organized in the modules/ folder.-----------------
-------The project separates simulation, configuration, and data transmission clearly, making it modular and maintainable.----------------

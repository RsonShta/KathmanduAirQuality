Kathmandu Air Quality Simulation Project

This project simulates air quality data for Kathmandu and sends it to ThingsBoard using MQTT. It is designed for learning, testing, and experimenting with IoT concepts without needing real sensors.

The system generates values for PM2.5, PM10, CO2, and NO2. Pollution levels increase during peak traffic hours (7–10 AM and 3–7 PM) and stay lower during normal hours. These values are sent continuously to ThingsBoard, where dashboards display the data and alarms are triggered when safe limits are exceeded.

Safe or normal limits for each pollutant (PM2.5, PM10, CO2, NO2) are defined in the `config.json` file. These values can be easily changed without modifying the main code, making the system flexible.

The project follows a simple and clean structure. The main script connects to ThingsBoard, collects simulated data, and sends it at regular intervals. The simulation logic is kept separate in another file, which keeps the code organized and easier to manage.

All important settings such as server details, device token, and data interval are stored in `config.json`. This separation ensures the code remains clean and easy to update.

Overall, the system is modular, beginner-friendly, and useful for understanding how IoT data flows from sensors to cloud platforms like ThingsBoard.

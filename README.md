🌿 Raspberry Project – Smart Houseplant Monitor & Home Automation

🧠 What It Does

This project monitors a houseplant's **temperature, air humidity, soil moisture** and remotely controls a **kitchen lightbulb** via wireless communication. It features **real-time** data logging, visualization, and now includes an OLED display for on-the-spot feedback.

🆕 **New feature**: Live OLED display for sensor data!

While it's currently controlled from a **desktop PC**, adjusting your modem settings allows access from **any device**.

---

🔩 Hardware Used

- Arduino Nano ESP32  
- DHT22 (temperature & humidity sensor)  
- Elecrow CT0007MS – Soil moisture sensor  
- Bestep 1-channel relay module  
- E27 lamp socket + bulb  
- Raspberry Pi 3B+  
- Modem with WiFi  
- Desktop PC  
- Jumper wires & breadboard  

---

💻 Software Stack

- Arduino IDE  
- Visual Studio Code  
- Raspbian (on Raspberry Pi)  
- Mosquitto MQTT broker  
- MariaDB (MySQL-compatible)  
- Python 3 & C++  

📦 Python Libraries (install with pip):

pip install paho-mqtt mysql-connector-python matplotlib SpeechRecognition

📚 Arduino Libraries (install via Arduino IDE):

WiFi

PubSubClient

DHT Sensor Library

ArduinoJson

🔌 System Overview

Arduino reads sensor values and publishes data via MQTT.

Raspberry Pi runs Mosquitto and subscribes to these MQTT topics.

Data is parsed and stored in MariaDB.

Python scripts pull and visualize the data (graphs, charts).

Another Python script allows sending messages that control a relay (turning lights on/off).

OLED screen shows sensor data in real-time.

Voice control via Google Web Speech API supports commands like "on" / "off".

📈 Files & Visuals

The Mosquitto MQTT-broker and MariaDB are running in raspberry to be clear.
![RASPBERRY MQTT drawio](https://github.com/user-attachments/assets/423cc79c-720c-4da1-924b-9512d51378bf)

Raspberry screen that shows raw data coming to it from Arduino, MariaDB with refined data, MQTT-broker's commands printed, and Mosquitto Configuration file.

 ![Raspberry_Screen](https://github.com/user-attachments/assets/bad0d5c6-cccf-49a7-b7a5-13e160dc3fb4)
 

Picture of Arduino, relay, DHT22 and CT0007MS.

 ![IMG_20250512_193713](https://github.com/user-attachments/assets/594e2884-1b37-4512-9ff4-e0b6e209720b)

 ![Data_5_6_25](https://github.com/user-attachments/assets/ceab0de0-2657-4816-abce-be7aa1dbde2e)

🛠️ Setup Guide (Coming Soon)
Step-by-step guides will cover:

Installing & configuring Mosquitto MQTT Broker

Setting up MariaDB and creating tables

Creating config files

Assigning a static IP to Raspberry Pi

All relevant Linux commands

🔭 Project Evolution (Storytime)
This all began as a side project to control a web radio using SSH on a Raspberry Pi. From there:

✅ LED indicators for SSH status

🌿 Initial attempt at an automated watering system using an aquarium pump

🌡️ Expansion into a weather station with DHT22 and air pressure sensors

💡 Building out MQTT message flow & data reliability

🛢️ Creating a MariaDB schema for structured data storage

🔄 MQTT message formatting using JSON

🎛️ Relay control logic triggered via MQTT

🗣️ Voice-controlled automation using Google's SpeechRecognition API

📶 Expanded to remote control via modem + PC + MQTT network

🗣️ Voice Control Highlights
Voice input is parsed by Python using Google Web Speech API.

Trigger keywords ("on", "off") control lights via MQTT → Raspberry Pi → Arduino relay.

Still being tuned to filter ambient noise more reliably.

⚙️ Technical Notes
MQTT messages flow in both directions:

Sensor → MQTT → MariaDB

Desktop → MQTT → Arduino (relay)

FreeRTOS is used on the ESP32 to handle multiple MQTT messages concurrently.

MQTT broker uses no password currently due to config challenges (future fix).

Soil moisture data is scaled to percent before storing.

🚧 In Development
More Arduinos joining the network

Multi-device MQTT load balancing

Web-based visualization dashboard

Extended voice interaction support

Real-time system status display

💬 Feedback & Contributions
This project is ongoing! Issues, ideas, pull requests, and discussions are welcome.

“Started with a blinking LED, and now I can voice-control my kitchen light—let’s see where this goes next!”

© 2025 Lassi | This project is a nerdy, evolving playground 🔧🌱

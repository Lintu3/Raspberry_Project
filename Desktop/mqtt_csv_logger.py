import csv
import json
import os
import time
import paho.mqtt.client as mqtt

# This script is a simple MQTT client that subscribes to a topic and writes incoming messages to a CSV file.

# MQTT Broker setting
broker_address = "broker_address"
topic = "sensoridata"

# CSV-file name
csv_filename = "sensori_data.csv"

# MQTT callback
# This function is called when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic)
    else:
        print("Connection failed with code", rc)
#def on_subscribe(client, userdata, mid, granted_qos):
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message}")
    write_to_csv(message)
# This function is called when a message is received on the subscribed topic
def parse_and_modify_temperature(message):
    # Parse the JSON message and modify the soil moisture value
    try:
        data = json.loads(message)
        original_moisture = data["soilmoisture"]
        modified_moisture =  round(calc_moisture(int(original_moisture))) # test
        print(f"----------")
        return modified_moisture
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None
# Function to calculate the soil moisture percentage
def calc_moisture(value, min=0, max=2600):
    if value <= min:
        return 0
    elif value >= max:
        return 100
    else:
        return (value - min) / (max - min) * 100

# Function to write the data to a CSV file
def write_to_csv(message):
    file_exists = os.path.isfile(csv_filename)
    mod_moisture = parse_and_modify_temperature(message)
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists or os.stat(csv_filename).st_size == 0:
            writer.writerow(["time", "temperature","humidity","soimoisture"])  # Add header if empty
        if message is not None:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([current_time, message["temperature"], message["humidity"], mod_moisture])

# create new MQTT-clientprogram
client = mqtt.Client("DesktopClient")

#define the MQTT callbacks and connect to the broker
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and wait for connection.
client.connect(broker_address, 1883, 60)
client.loop_forever()

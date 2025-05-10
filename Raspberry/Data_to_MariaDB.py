import json
import paho.mqtt.client as mqtt
import mysql.connector

# Establishing a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="yyyy",
    password="????",
    database="xxxx"
)

# Creating a cursor object to interact with the database
cursor =db.cursor()

# Defining the MQTT broker address (localhost in this case) and MQTT topic
broker_address = "127.0.0.1"
topic = "sensoridata"

# Function to handle incoming MQTT messages
def on_message(client, userdata, message):
    # Decoding the payload of the received message
    payload = message.payload.decode()
    print(f'Payload: {payload}')
    # Parsing the JSON data from the payload
    data = json.loads(payload)
    # Extracting the soil moisture value from the parsed data and converting it to an integer
    # Calculating the soil moisture percentage using the calc function
    soilmoisture = data["soilmoisture"]
    soilmoisture = int(soilmoisture)
    soilmoisture =round(calc(soilmoisture),2)
    # Extracting the temperature and humidity values from the parsed data
    temperature = data["temperature"]
    humidity = data["humidity"]
    # Inserting the data into the database
    cursor.execute("INSERT INTO xxxx_table (temperature, humidity, soilmoisture) VALUES (%s,%s,%s)",(temperature,humidity,soilmoisture))
    db.commit()

# Function to calculate the soil moisture percentage
def calc(soil, min=0, max=2600):
    if soil <= min:
        return 0
    elif soil >= max:
        return 100
    else:
        return (soil-min)/(max-min)*100

# Creating an MQTT client instance with a specific client ID and protocol version
client = mqtt.Client(client_id="RaspCl", protocol=mqtt.MQTTv311)
client.on_message = on_message
client.connect(broker_address)

# Subscribing to the specified MQTT topic
client.subscribe(topic)
client.loop_forever()
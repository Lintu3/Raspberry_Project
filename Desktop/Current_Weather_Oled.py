import paho.mqtt.client as mqtt
import requests
import time

broker = "192.168.1.102"  # Change to your broker's IP
port = 1883
topic = "oled/display"

# Weather API settings
OWM_API_KEY = "************************"  # Change to your OpenWeatherMap API key"
CITY = "CITY"  # Change to your city
COUNTRY = "country"     # Change to your country code

# Function to send a message to the MQTT broker
def send_message(message):
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(broker, port, 60)
    client.publish(topic, message)
    client.disconnect()
    print(f"Sent: {message}")

# Function to get the current weather from OpenWeatherMap API
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY}&appid={OWM_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        print(data)  
        if "main" in data and "weather" in data: 
            temp = data["main"]["temp"] 
            desc = data["wind"]["speed"] 
            weather_msg = f"temp:{temp:.1f}C,wind: {desc}"
            return weather_msg
        else:
            return "Weather: unavailable"
    except Exception as e:
        return f"Weather error: {e}"
    
if __name__ == "__main__":
    while True:
        weather = get_weather()
        send_message(weather)
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)
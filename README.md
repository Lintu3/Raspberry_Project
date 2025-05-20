Currently the project measures temperature, airmoisture, soilmoisture of a houseplant and turns on a lightpulp in my kitchen. It's using wireless connection. It's controlled from desktop PC but with small adjustment to modem settings it's possible to control it from and receive data to any device.

Project involvolves Arduino Nano ESP32, Raspberry Pi 3B+, MQTT-protocol and MariaDB.
The codes have comments and here is some explanation of the system.
Project is set up and working as intended.

Here you can see a rough diagram about it.  
![Project_Diagram(2)](https://github.com/user-attachments/assets/90c65834-e344-480d-9732-3623bddbb819)  
The Mosquitto MQTT-broker and MariaDB are running in raspberry to be clear.

Added one picture of drawn data, check the files for ArduinoData.png. it has a cap in April 17.-21. and small cap after it because I was testing things and had wifi off.

Still in development. 

What I worked with:

Hardware:  
Arduino Nano ESP32,  
Bestep 1-channel relay module,  
DHT22 temperature and airmoisture sensor,  
Elecrow CT0007MS - Moisture Sensor 2.0,  
some wires,  
E27 socket and lamp,  
Raspberry Pi 3B+,  
Modem with wifi 
and desktop PC.

Software:  
Arduino IDE,  
Visual studio code,  
Raspbian that came with Raspberry Pi,  
Mosquitto MQTT broker,  
MySQL MariaDB,  
Python and C++.  

Librarys:  
install with pip for python:  
paho-mqtt,  
mysql-connector-python,  
matplotlib,  
SpeechRecognition.  

install in Arduino IDE:  
WiFi,  
PubSubClient,  
DHT sensor library,  
ArduinoJson

Step by step instructions are coming later. Those include installation of Mosquitto, MariaDB etc. and config file setup, also static IP-address for wireless network for Raspberry. I will add all of the Linux commands that are needed.

Story about the project evolving:

I had a Raspberry PI 3B+ that was working as a radio and I thought that it would be cool to start making some code or system settings. I knew of the endless possibilities that could be done with it and I wasn't sure what to do.

 I started experimenting on SSH-connection to remotely control web radio and after I got it working with my phone I wanted more. I ordered some resistors, LEDs and wires. I experimented with them to turn LED on if SSH-connection was on, so I could see quickly if I accidentaly was still connected. Next I figured that I want something like automated houseplant watering system or something like that... 

I have an old aquarium pump and I figured that I need something to control it with. I decided that a relay, arduino and soilmoisture sensor would do. I ordered those. When they arrived I got it working quite fast as I had planned it before hand. But there was a problem, where can I get water automaticaly. I live in a rental residence so pluming was not an option. I still have the code from that project but I tossed it. 

Next up I figured that maybe I could make a automated weather station (still on my mind). So I ordered a DHT22 air temperature/moisture sensor and a air pressure sensor (it's still in plastic). Now I needed to figure a reliable way to get the data from that sensor and have it stored somewhere.

First I made the arduino send kinda stupid data to raspberry and have it print it in .csv to store it. That worked as expected and I could do a graph from that .csv but I figured that it's not reliable or the correct way to do it. So I started figuring how to send large amounts of data with low bandwith from a distance.  

I decided that MQTT-protocol is the way to go. I decided to send a JSON message with 3 different kinds of info: soilmoisture/temperature/airmoisture. 

Okey now I got that figured so where am I going to send and store the data? Well MySQL database ofcourse. So set up MariaDB on raspberry with one table that has timestamp,soilmoisture,temperature and airmoisture colums.

 I had to figure how MQTT message is used so I installed Mosquitto MQTT-broker on Raspberry as well. Then created the subscription that receives that JSON that I mentioned. There was a curious problems with connection and it had to do with the Mosquitto config file. There is something wrong with the broker when I had password set up(going to figure out later), so I just left that out for now. Okey so now I had to make a script that takes that JSON, formats it a bit because the soilmoisture value was just numbers with a range of 0 to ~2500. 
Where as 0 is just air and ~2500 pure water... 

The script Data_to_MariaDB calculates percents from that to get it right and stores it to the MariaDB.  
Hurray it works!

Now I made another script with my desktop PC to access that Raspberry via MySQL.connector connection to retrieve the data for analysis. I then used the data with matplotlib to create a graph you can checkout the .png file. 

Okey nice now I can analyse my home temperature, humidity and house plant soil. Well I got hungry for more. Remember the relay I had, well I thought that if I can send data with Arduino to Raspberry maybe I can do it otherway around as well? To the arduino code->.

 There I made a callback (actually I already had one because of debugging) for receiving data via MQTT. Okey so now I know it works. I made a new subscription for the MQTT-broker in Raspberry and made the arduinos callback function to receive something. 

Well I connected the relay and made it control a lamp in my kitchen. So I wrote a script (tcp_mqtt_bridge) in raspberry to receive a message, a simple string "on"/"off" and made the MQTT-broker to send that same string to arduino and when it arrives the callback function gives a singal to relay to turn either on or off. 

Right, now I had that figured so I made a script to my desktop PC so I can type either "on" or "off" and it sends it to raspberry and so on. Until relay switches the light on or off. 

Now I have remote control to my kitchen light. 
Cool! 

As I mentioned before this thing is evolving and I'm making voice control system for it now. It's currently working with Google voice recognition API and I set the key words by my self. The code is kinda funny looking because its still a test. It works really well but sometimes the ambient sound filter thing makes it not recognice my words if I don't speak loudly.

Now I'm waiting for more Arduinos to arrive and some other stuff. I want to try making a bigger network of things and see if Raspberry can handle the load from multiple sources. Let's see what I come up with. :) 

This will continue...

More info when I have time between working.

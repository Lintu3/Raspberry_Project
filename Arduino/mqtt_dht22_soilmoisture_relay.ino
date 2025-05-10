#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h> 
#include <ArduinoJson.h>

// DHT22 sensor
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// WiFi and MQTT settings
const char* ssid = "xxxx"; //Wifi name
const char* password = "????"; // password
const char* mqtt_server = "00.00.00.00"; // MQTT-address IP...
//const char* mqtt_user = "";
//const char* mqtt_password = "";

// Sensor settings
const int soilSensorPin = A0; // Soilmoisture signalpin (analog)
const int relayPin = 2; // Relay singnalpin (digi)

// MQTT settings
WiFiClient espClient;
PubSubClient client(espClient);

// Relay settings
unsigned long previousMillis = 0; 
const long interval = 5000; // 5 seconds


void setup() {
  pinMode(relayPin, OUTPUT); // define relay singalpin
  digitalWrite(relayPin, LOW); // Make sure relay is off
  WiFi.disconnect(); // I'm not sure if this is even needed
  Serial.begin(115200); // 9600 or 115200 
  delay(1500);

  Serial.print("Wifi status: ");
  Serial.println(WiFi.status());

  WiFi.begin(ssid, password); //Wifi connection start
  Serial.println("Connecting to WiFi....");

  Serial.print("Wifi status: ");
  Serial.println(WiFi.status());
  // Try to connect to wifi

  // Check if success
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } 
  else {
    Serial.println("Failed to connect to WiFi");
    // If failed
    Serial.println("Retrying...");
  }
  while (WiFi.status() != WL_CONNECTED ) {
    delay(1000);
    Serial.print("Connecting...");
    Serial.print("Wifi status: ");
    Serial.println(WiFi.status());
    
  }
  // If connected
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  }
  client.setServer(mqtt_server, 1883); //MQTT address and port
  //client.setCallback(callback); // MQTT message callback.
  client.setCallback(callback); 
  
  dht.begin(); // start DHT22
}


void loop() {
  // Check connection is still on
  if(WiFi.status() != WL_CONNECTED){
    ReconnectWifi();
  }

  if (!client.connected()) { //loop MQTT connection if not on 
    reconnect();
  }
  client.loop();
    // Get current time
  unsigned long currentMillis = millis();

  // Execute sensor reading and publishing at specified interval
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    // Read DHT22 sensor
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
  // Check if any reads failed and exit early (to try again).
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return; 
  }
  // Print temperature and humidity
  int soilMoistureValue = analogRead(soilSensorPin); // Read soil moisture
  Serial.print("----- ");
  // NEEDS optimising calculation done in rasperry. 
   Serial.println();
 
   StaticJsonDocument<200> doc; //JSON message creation
  doc["soilmoisture"] = soilMoistureValue; 
  doc["temperature"] = temperature; 
  doc["humidity"] = humidity; 

  char buffer[256]; size_t n = serializeJson(doc, buffer); 
  client.publish("sensoridata", buffer, n); // JSON message send to MQTT-broker

  Serial.print("Published: "); 
  Serial.println(buffer);

  }
}

// Callback function to handle incoming messages
void callback(char* topic, byte* payload, unsigned int length) {  
//Used to send a command to turn on relay.
    payload[length] = '\0';
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    Serial.println();
    String message = String((char*)payload);
    Serial.println(message);
    if (message == "on") {
      digitalWrite(relayPin, HIGH);
      Serial.println("Relay ON"); 
    } 
    else if (message == "off") {
      digitalWrite(relayPin, LOW);
      Serial.println("Relay OFF"); 
    }
  
}

// Function to reconnect to WiFi if disconnected
void ReconnectWifi(){ 
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Lost WiFi connection. Attempting to reconnect...");
    Serial.print("Wifi status: ");
    Serial.println(WiFi.status());
    WiFi.begin(ssid, password);
    int max_attempts = 40;
    int attempts = 0;
    // Try to connect to wifi
    while (WiFi.status() != WL_CONNECTED && attempts < max_attempts) {
      delay(1000);
      Serial.print("Connecting...");
      Serial.print("Wifi status: ");
      Serial.println(WiFi.status());
      attempts++;
    }
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("WiFi reconnected");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
    } 
    else {
      Serial.println("Reconnection failed.");
      delay(5000); // wait 5 sec 
    }
  }
}
// Function to reconnect to MQTT broker if disconnected
void reconnect() { 
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) { //mqtt_user, mqtt_password can be added here.
      Serial.println("connected");
     // client.subscribe("sensoridata");
      client.subscribe("relaylamp");
      delay(5000);
    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

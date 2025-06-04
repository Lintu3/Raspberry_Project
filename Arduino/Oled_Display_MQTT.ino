#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const char* ssid = "xxxx"; // Change to your WiFi SSID
const char* password = "??????"; // Change to your WiFi credentials
const char* mqtt_server = "192.168.1.102"; // Change to your broker IP

// Create a WiFi client and PubSubClient instance
WiFiClient espClient;
PubSubClient client(espClient);

// OLED message buffer
#define MAX_LINES 3
#define MAX_MSG_LEN 42

// Structure to hold messages for OLED display
typedef struct {
  char text[MAX_MSG_LEN];
} OledMsg;

// Global variables
OledMsg msgBuffer[MAX_LINES];
int msgCount = 0;
String latestTemp = "--";

QueueHandle_t oledQueue;

// Function to print the message buffer to the OLED display
void printBufferToOled() {
  display.clearDisplay();
  display.setTextSize(1.2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("Temperature: ");
  display.println(latestTemp);
  int y = 16;
  for (int i = 0; i < msgCount; i++) {
    display.setCursor(0, y);
    display.println(msgBuffer[i].text);
    y += 12;
  }
  display.display();
}

// Callback function for MQTT messages
void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';
  String message = String((char*)payload);

  // Handle different topics
  if (String(topic) == "sensoridata") {
    // Try to parse as JSON and extract temperature
    StaticJsonDocument<128> doc;
    DeserializationError error = deserializeJson(doc, message);
    if (!error && doc.containsKey("temperature")) {
      float temp = doc["temperature"];
      latestTemp = String(temp, 1) + " C";
    } else {
      latestTemp = "--";
    }
    printBufferToOled();
    // Add the latest temperature to the message buffer
  } else if (String(topic) == "oled/display") {
    OledMsg oledMsg;
    memset(&oledMsg, 0, sizeof(oledMsg));
    message.toCharArray(oledMsg.text, sizeof(oledMsg.text));
    xQueueSend(oledQueue, &oledMsg, 0);
  }
}

// Task to handle MQTT connection and message processing
void mqttTask(void *pvParameters) {
  for (;;) {
    if (!client.connected()) {
      while (!client.connected()) {
        if (client.connect("OledClient")) {
          client.subscribe("sensoridata");
          client.subscribe("oled/display");
        } else {
          vTaskDelay(2000 / portTICK_PERIOD_MS);
        }
      }
    }
    client.loop();
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

// Task to handle OLED display updates
void oledTask(void *pvParameters) {
  OledMsg oledMsg;
  for (;;) {
    if (xQueueReceive(oledQueue, &oledMsg, portMAX_DELAY) == pdTRUE) {
      // Shift buffer up if full
      if (msgCount == MAX_LINES) {
        for (int i = 1; i < MAX_LINES; i++) {
          msgBuffer[i - 1] = msgBuffer[i];
        }
        msgCount--;
      }
      // Add new message
      msgBuffer[msgCount++] = oledMsg;
      printBufferToOled();
    }
  }
}

// Setup function to initialize WiFi, MQTT, and OLED display
void setup() {
  Serial.begin(115200);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (1);
  }
  display.clearDisplay();
  display.display();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // Initialize MQTT client
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Initialize OLED message queue
  oledQueue = xQueueCreate(5, sizeof(OledMsg));
  xTaskCreate(mqttTask, "MQTT Task", 4096, NULL, 1, NULL);
  xTaskCreate(oledTask, "OLED Task", 2048, NULL, 1, NULL);
}

void loop() {
  // FreeRTOS tasks handle everything
}
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

const char* WIFI_SSID = "DTU";
const char* WIFI_PASSWORD = "";

const char* MQTT_SERVER = "172.28.156.95";
const int MQTT_PORT = 1883;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(DHTPIN, DHTTYPE);

void connectWiFi() {
  Serial.print("Connecting to WiFi");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT...");

    String clientId = "ESP32-DHT11-";
    clientId += String(random(0xffff), HEX);

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, state=");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  dht.begin();

  connectWiFi();

  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  if (!mqttClient.connected()) {
    connectMQTT();
  }

  mqttClient.loop();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read DHT11");
    delay(2000);
    return;
  }

  char temperatureText[10];
  char humidityText[10];

  dtostrf(temperature, 1, 2, temperatureText);
  dtostrf(humidity, 1, 2, humidityText);

  mqttClient.publish(
    "esp32/dht11/temperature",
    temperatureText,
    true
  );

  mqttClient.publish(
    "esp32/dht11/humidity",
    humidityText,
    true
  );

  Serial.print("Temperature: ");
  Serial.print(temperatureText);
  Serial.println(" C");

  Serial.print("Humidity: ");
  Serial.print(humidityText);
  Serial.println(" %");

  delay(5000);
}

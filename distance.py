#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// 1. Cấu hình WiFi và MQTT Broker (Raspberry Pi chạy OpenHAB)
const char* ssid = "TEN_WIFI";
const char* password = "MK_WIFI";
const char* mqtt_server = "IP_RASPBERRY_PI"; // IP của Pi chạy OpenHAB

#define DHTPIN 4          // Chân Data của DHT11 nối với GPIO4 trên ESP32
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Kết nối WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // Cấu hình MQTT
  client.setServer(mqtt_server, 1883);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32_DHT11_Client")) {
      Serial.println("MQTT connected");
    } else {
      delay(2000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Đọc nhiệt độ và độ ẩm từ DHT11
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (!isnan(h) && !isnan(t)) {
    // Bắn dữ liệu lên các Topic MQTT để OpenHAB nhận
    client.publish("esp32/dht11/temperature", String(t).c_str());
    client.publish("esp32/dht11/humidity", String(h).c_str());

    Serial.print("Nhiệt độ: "); Serial.print(t);
    Serial.print(" °C | Độ ẩm: "); Serial.print(h); Serial.println(" %");
  }

  delay(5000); // Gửi dữ liệu mỗi 5 giây
}

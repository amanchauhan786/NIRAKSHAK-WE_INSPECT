#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <DHT.h>
#include <SoftwareSerial.h>

// WiFi Credentials
const char *ssid = "My-Network";
const char *password = "aniket123";

// Sensor Pins
#define MQ135_PIN  4  // Analog input for MQ135 (A0)
#define DHT_PIN    14  // DHT11 sensor
#define FLAME_PIN  12  // Digital input for flame sensor
#define TX_PIN     43  // GPS TX (ESP32-RX)
#define RX_PIN     44  // GPS RX (ESP32-TX)

// Thresholds
#define SAFE_CO2_LEVEL  400   // Safe CO2 level in PPM
#define DANGER_CO2_LEVEL 1000 // Danger level CO2

// DHT Sensor Setup
#define DHT_TYPE DHT11
DHT dht(DHT_PIN, DHT_TYPE);

// GPS Module (Neo 6M)
SoftwareSerial gpsSerial(TX_PIN, RX_PIN);  // Serial for GPS

// Web Server
WebServer server(80);

void handleRoot() {
    char msg[2000]; // Increased buffer size for more sensor data

    snprintf(msg, 2000,
             "<html>\
  <head>\
    <meta http-equiv='refresh' content='2'/>\
    <meta name='viewport' content='width=device-width, initial-scale=1'>\
    <title>ESP32 Sensor Data</title>\
    <style>\
    body { font-family: Arial; text-align: center; background: #f4f4f4; padding: 20px;}\
    h2 { font-size: 2.5rem; color: #333;}\
    .data-box { background: white; padding: 20px; margin: 10px auto; width: 50%%; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);}\
    .status-safe { color: green; font-weight: bold; }\
    .status-warning { color: orange; font-weight: bold; }\
    .status-danger { color: red; font-weight: bold; }\
    </style>\
  </head>\
  <body>\
      <h2>ESP32 Sensor Monitoring</h2>\
      <div class='data-box'>\
        <p><strong>Temperature:</strong> %.2f °C</p>\
        <p><strong>Humidity:</strong> %.2f %%</p>\
        <p><strong>CO2 Status:</strong> <span class='%s'>%s</span></p>\
        <p><strong>Flame Sensor:</strong> %s</p>\
        <p><strong>GPS:</strong> %s</p>\
      </div>\
  </body>\
</html>",
             readDHTTemperature(),
             readDHTHumidity(),
             getCO2StatusClass(), getCO2Status(),
             readFlameSensor(),
             getGPSData()
            );
    server.send(200, "text/html", msg);
}

void setup() {
    Serial.begin(115200);
    gpsSerial.begin(9600);
    dht.begin();

    pinMode(FLAME_PIN, INPUT);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting to WiFi...");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nConnected to WiFi");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    if (MDNS.begin("esp32")) {
        Serial.println("MDNS responder started");
    }

    server.on("/", handleRoot);
    server.begin();
    Serial.println("HTTP Server Started");
}

void loop() {
    server.handleClient();
    delay(1);  // Allow CPU to process other tasks
}

// Function to Read Temperature from DHT11
float readDHTTemperature() {
    float t = dht.readTemperature();
    if (isnan(t)) {
        Serial.println("Failed to read temperature!");
        return -1;
    }
    return t;
}

// Function to Read Humidity from DHT11
float readDHTHumidity() {
    float h = dht.readHumidity();
    if (isnan(h)) {
        Serial.println("Failed to read humidity!");
        return -1;
    }
    return h;
}

// Function to Read and Classify CO2 Status
String getCO2Status() {
    int mq135Value = analogRead(MQ135_PIN);
    Serial.print("MQ135 Reading: ");
    Serial.println(mq135Value);

    if (mq135Value > DANGER_CO2_LEVEL) {
        return "Safe";
    } else if (mq135Value > SAFE_CO2_LEVEL) {
        return "Warning";
    }
    return "Dangerous";
}

// Function to Assign Color Class for CO2 Status
const char* getCO2StatusClass() {
    String status = getCO2Status();
    if (status == "DANGEROUS") {
        return "status-danger";
    } else if (status == "Warning") {
        return "status-warning";
    }
    return "status-safe";
}

// Function to Read Flame Sensor Status
const char* readFlameSensor() {
    int flameState = digitalRead(FLAME_PIN);
    return (flameState == LOW) ? "FIRE DETECTED!" : "No Fire";
}

// Function to Read GPS Data
String getGPSData() {
    String gpsInfo = "";
    while (gpsSerial.available()) {
        char c = gpsSerial.read();
        gpsInfo += c;
    }
    return gpsInfo.length() > 0 ? gpsInfo : "No GPS Data";
}

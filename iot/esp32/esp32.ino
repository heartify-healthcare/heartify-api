/****************************************
 * Heart Disease Prediction IoT System
 * Combined AD8232 ECG + MAX30102 Heart Rate
 * With HTTP Server for Mobile App Integration
 ****************************************/

#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

/****************************************
 * WiFi Configuration
 ****************************************/
const char* ssid = "UT PHI";        // Replace with your WiFi SSID
const char* password = "conkhongbietanhhaidat"; // Replace with your WiFi password

/****************************************
 * Server Configuration
 ****************************************/
WebServer server(80);
const char* flaskServerURL = "http://192.168.1.20:5000/predictions/heart-disease";

/****************************************
 * AD8232 ECG Configuration
 ****************************************/
#define ECG_PIN    34  // ESP32 analog input pin for the AD8232 output
#define LO_PLUS    32  // Lead-off detection LO+
#define LO_MINUS   35  // Lead-off detection LO-

/****************************************
 * ECG Buffer Configuration
 ****************************************/
const int ECG_BUFFER_SIZE = 1000;  // 10 seconds * 100 samples/second
int ecgBuffer[ECG_BUFFER_SIZE];
int ecgBufferIndex = 0;
unsigned long lastECGRead = 0;
const unsigned long ECG_SAMPLE_INTERVAL = 4; // 4ms = 250Hz sampling rate

/****************************************
 * MAX30102 Heart Rate Configuration
 ****************************************/
MAX30105 particleSensor;
const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute = 0;
int beatAvg = 0;
int maxHeartRate = 0; // thalach - maximum heart rate recorded

/****************************************
 * System Status
 ****************************************/
bool wifiConnected = false;
bool max30102Connected = false;
bool leadsConnected = false;

/****************************************
 * Setup Function
 ****************************************/
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== Heart Disease Prediction IoT System ===");
  Serial.println("Initializing...");
  
  // Initialize AD8232 pins
  pinMode(ECG_PIN, INPUT);
  pinMode(LO_PLUS, INPUT);
  pinMode(LO_MINUS, INPUT);
  
  // Initialize ECG buffer
  for (int i = 0; i < ECG_BUFFER_SIZE; i++) {
    ecgBuffer[i] = 0;
  }
  
  // Initialize MAX30102
  if (particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 sensor initialized successfully");
    particleSensor.setup();
    particleSensor.setPulseAmplitudeRed(0x0A);
    particleSensor.setPulseAmplitudeGreen(0);
    max30102Connected = true;
  } else {
    Serial.println("MAX30102 sensor initialization failed!");
    max30102Connected = false;
  }
  
  // Initialize WiFi
  initWiFi();
  
  // Setup HTTP server endpoints
  setupServerEndpoints();
  
  // Start HTTP server
  server.begin();
  Serial.println("HTTP server started on port 80");
  Serial.println("System ready for operation");
  Serial.println("Place finger on MAX30102 sensor for heart rate monitoring");
}

/****************************************
 * Main Loop
 ****************************************/
void loop() {
  // Handle HTTP server requests
  server.handleClient();
  
  // Read ECG data
  readECGData();
  
  // Read heart rate data
  readHeartRateData();
  
  // Small delay to prevent watchdog timeout
  delay(1);
}

/****************************************
 * WiFi Initialization
 ****************************************/
void initWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println();
    Serial.println("WiFi connected successfully");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiConnected = false;
    Serial.println();
    Serial.println("WiFi connection failed!");
  }
}

/****************************************
 * HTTP Server Endpoints Setup
 ****************************************/
void setupServerEndpoints() {
  // Health check endpoint
  server.on("/", HTTP_GET, []() {
    String response = "Heart Disease Prediction IoT System\n";
    response += "Status: " + String(wifiConnected ? "Connected" : "Disconnected") + "\n";
    response += "MAX30102: " + String(max30102Connected ? "Connected" : "Disconnected") + "\n";
    response += "ECG Leads: " + String(leadsConnected ? "Connected" : "Check connections") + "\n";
    response += "Current Heart Rate: " + String(beatsPerMinute) + " BPM\n";
    response += "Max Heart Rate: " + String(maxHeartRate) + " BPM\n";
    server.send(200, "text/plain", response);
  });
  
  // Main prediction endpoint
  server.on("/submit", HTTP_POST, handlePredictionRequest);
  
  // Enable CORS for all endpoints
  server.enableCORS(true);
}

/****************************************
 * ECG Data Reading
 ****************************************/
void readECGData() {
  unsigned long currentTime = millis();
  
  // Check if it's time to read ECG (100Hz sampling)
  if (currentTime - lastECGRead >= ECG_SAMPLE_INTERVAL) {
    lastECGRead = currentTime;
    
    // Check if leads are properly connected
    if (digitalRead(LO_PLUS) == 1 || digitalRead(LO_MINUS) == 1) {
      leadsConnected = false;
      // Store 0 for disconnected leads
      ecgBuffer[ecgBufferIndex] = 0;
    } else {
      leadsConnected = true;
      // Read ECG signal value
      int ecgValue = analogRead(ECG_PIN);
      ecgBuffer[ecgBufferIndex] = ecgValue;
    }
    
    // Move to next buffer position (circular buffer)
    ecgBufferIndex = (ecgBufferIndex + 1) % ECG_BUFFER_SIZE;
  }
}

/****************************************
 * Heart Rate Data Reading
 ****************************************/
void readHeartRateData() {
  if (!max30102Connected) return;
  
  long irValue = particleSensor.getIR();
  
  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    
    beatsPerMinute = 60 / (delta / 1000.0);
    
    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;
      
      // Calculate average
      beatAvg = 0;
      for (byte x = 0; x < RATE_SIZE; x++) {
        beatAvg += rates[x];
      }
      beatAvg /= RATE_SIZE;
      
      // Update maximum heart rate (thalach)
      if (beatAvg > maxHeartRate) {
        maxHeartRate = beatAvg;
      }
    }
  }
}

/****************************************
 * Handle Prediction Request
 ****************************************/
void handlePredictionRequest() {
  Serial.println("Received prediction request");
  
  // Check if WiFi is connected
  if (!wifiConnected) {
    server.send(500, "application/json", "{\"success\":false,\"message\":\"WiFi not connected\"}");
    return;
  }
  
  // Parse JSON request
  String requestBody = server.arg("plain");
  DynamicJsonDocument requestDoc(1024);
  DeserializationError error = deserializeJson(requestDoc, requestBody);
  
  if (error) {
    Serial.println("Failed to parse JSON request");
    server.send(400, "application/json", "{\"success\":false,\"message\":\"Invalid JSON\"}");
    return;
  }
  
  // Extract values from request
  int age = requestDoc["age"];
  int sex = requestDoc["sex"];
  int cp = requestDoc["cp"];
  int trestbps = requestDoc["trestbps"];
  int exang = requestDoc["exang"];
  String accessToken = requestDoc["access_token"];
  
  Serial.printf("Received data - Age: %d, Sex: %d, CP: %d, BP: %d, Exang: %d\n", 
                age, sex, cp, trestbps, exang);
  
  // Check if access token is provided
  if (accessToken.length() == 0) {
    Serial.println("No access token provided");
    server.send(400, "application/json", "{\"success\":false,\"message\":\"Access token required\"}");
    return;
  }
  
  // Prepare ECG array for transmission
  JsonArray ecgArray;
  DynamicJsonDocument payloadDoc(8192); // Larger buffer for ECG data
  
  payloadDoc["age"] = age;
  payloadDoc["sex"] = sex;
  payloadDoc["cp"] = cp;
  payloadDoc["trestbps"] = trestbps;
  payloadDoc["exang"] = exang;
  payloadDoc["thalach"] = maxHeartRate;
  
  // Add ECG data array
  ecgArray = payloadDoc.createNestedArray("ecg");
  for (int i = 0; i < ECG_BUFFER_SIZE; i++) {
    int index = (ecgBufferIndex + i) % ECG_BUFFER_SIZE; // Get data in chronological order
    ecgArray.add(ecgBuffer[index]);
  }
  
  Serial.println("Sending prediction request to Flask server...");
  Serial.printf("Thalach (max heart rate): %d\n", maxHeartRate);
  Serial.printf("ECG buffer contains %d samples\n", ECG_BUFFER_SIZE);
  
  // Send POST request to Flask server
  HTTPClient http;
  http.begin(flaskServerURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + accessToken);  // Add Bearer token
  
  String payload;
  serializeJson(payloadDoc, payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.printf("Flask server response code: %d\n", httpResponseCode);
    Serial.printf("Flask server response: %s\n", response.c_str());
    
    // Forward the response to the mobile app
    server.send(httpResponseCode, "application/json", response);
  } else {
    Serial.printf("Error sending request to Flask server: %d\n", httpResponseCode);
    String errorResponse = "{\"success\":false,\"message\":\"Failed to communicate with prediction server\"}";
    server.send(500, "application/json", errorResponse);
  }
  
  http.end();
}

/****************************************
 * Utility Functions
 ****************************************/
void printSystemStatus() {
  Serial.println("=== System Status ===");
  Serial.printf("WiFi: %s\n", wifiConnected ? "Connected" : "Disconnected");
  Serial.printf("MAX30102: %s\n", max30102Connected ? "Connected" : "Disconnected");
  Serial.printf("ECG Leads: %s\n", leadsConnected ? "Connected" : "Check connections");
  Serial.printf("Current BPM: %.1f\n", beatsPerMinute);
  Serial.printf("Average BPM: %d\n", beatAvg);
  Serial.printf("Max Heart Rate: %d\n", maxHeartRate);
  Serial.printf("ECG Buffer Index: %d\n", ecgBufferIndex);
  Serial.println("==================");
}
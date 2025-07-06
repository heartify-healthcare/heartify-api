/****************************************
 * Define Constants
 ****************************************/

// AD8232 pins
#define ECG_PIN    34  // ESP32 analog input pin for the AD8232 output
#define LO_PLUS    32  // Lead-off detection LO+
#define LO_MINUS   35  // Lead-off detection LO-

/****************************************
 * Setup
 ****************************************/
void setup() {
  Serial.begin(115200);  // Start serial communication for monitoring
  
  // Configure AD8232 pins
  pinMode(ECG_PIN, INPUT);      // ECG signal
  pinMode(LO_PLUS, INPUT);      // Lead-off detection LO+
  pinMode(LO_MINUS, INPUT);     // Lead-off detection LO-

  Serial.println("ECG Monitoring System Ready...");
}

/****************************************
 * Main Loop
 ****************************************/
void loop() {
  // Check if leads are properly connected
  if (digitalRead(LO_PLUS) == 1 || digitalRead(LO_MINUS) == 1) {
    Serial.println("Leads off or not properly connected!");
  } else {
    // Read ECG signal value
    int ecgValue = analogRead(ECG_PIN);

    // Display raw ECG value
    Serial.println(ecgValue);
    // Serial.print(",");
  }

  delay(4);  // Adjust delay for sampling rate (e.g. ~250Hz)
}

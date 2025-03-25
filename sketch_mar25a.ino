void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
}

void loop() {
    if (Serial.available()) { // Check if data is available
        String data = Serial.readStringUntil('\n'); 
        Serial.print("Received: "); 
        Serial.println(data); 
    }
}

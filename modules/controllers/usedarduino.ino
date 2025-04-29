void setup() {
    pinMode(13, OUTPUT);
    Serial.begin(9600);
    delay(1000);
  }
  
  void loop() {
    if (Serial.available() > 0) {
      //delay(0);
      byte received = Serial.read();
      digitalWrite(13, HIGH);
      Serial.write(received);
      //delay(5000);           // Stay on for 10 seconds
      digitalWrite(13, LOW);  // Then off again
    }
  }
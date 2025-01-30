// Define the connections pins
#define TRIG_PIN 7
#define ECHO_PIN 6

void setup() {
  // Initialize serial communication:
  Serial.begin(9600);
  // Define pin modes:
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  
  float dist = distanceMeasure();
  // Print the distance on the Serial Monitor:
  Serial.print("Distance: ");
  Serial.print(dist);
  Serial.println(" cm");

  // Delay 50ms before next measurement:
  delay(50);
}

float distanceMeasure(){
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(5);
  // Trigger the sensor by setting the trigPin high for 10 microseconds:
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(100);
  digitalWrite(TRIG_PIN, LOW);
  
  // Read the echoPin, returns the sound wave travel time in microseconds
  unsigned long duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calculate the distance:
  float distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  return distance;
}

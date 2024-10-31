int xPin = A0;
int yPin = A1;
int buttonPin = A2;
int xVal; // variable for storing joystick x values
int yVal; // variable for storing joystick y values
int switchState; // variable for storing joystick switch state
 
void setup() {
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600); // initialize the serial monitor
}
 
void loop() {
  // read the x, y and joystick switch values
  xVal = analogRead(xPin);
  yVal = analogRead(yPin);
  switchState = digitalRead(buttonPin);
 
  // print readings to the serial monitor
  Serial.print("X: ");
  Serial.print(xVal);
  Serial.print(" | Y: ");
  Serial.print(yVal);
  Serial.print(" | Switch: ");
  Serial.println(switchState);
 
  delay(100);
}
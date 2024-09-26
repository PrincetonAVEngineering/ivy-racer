
void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() == 0){
    String input = Serial.readString();
    char control = input.charAt(0);
    
    switch(control){
      case 'w':
        Serial.println("forward");
        break;

      case 'a':
        Serial.println("left");
        break;

      case 's':
        Serial.println("reverse");
        break;
        
      case 'd':
        Serial.println("right");
        break;

      default:
        break;
    }
  }
  delay(10);
}
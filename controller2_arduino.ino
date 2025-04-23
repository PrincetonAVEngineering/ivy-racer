float currentAngle = 0.0;
char currentDir = 'R';
const int pulsePin = 3;
const int dirPin = 2;

const int STEPS_ONE_REV = 200;
int curr_pos = 0;

int targetAngle = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Send ready message
  Serial.println("Arduino ready!");

  pinMode(pulsePin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}


void loop() {
  //rotateByAngle(30);
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming string until newline
    String data = Serial.readStringUntil('\n');
    
    // Parse the received data
    if (parseCommand(data)) {
      // Send acknowledgment with current values
      Serial.println("ACK:ANGLE:");
      Serial.println(targetAngle);
      Serial.println("ACK:DIR:");
      Serial.println(currentDir);

      int offset = (targetAngle - currentAngle);
      //Serial.p
      if (currentDir == 'R') {
         digitalWrite(dirPin, HIGH);    
      }else {
         digitalWrite(dirPin, LOW);  //low ccw? 
      }
      
      /*
       // Set direction //High is Clockwise, Low is CCW
      if(offset < 0){
        digitalWrite(dirPin, LOW);
      }
      else { 
        digitalWrite(dirPin, HIGH);
      }*/


      rotateByAngle(offset);
      currentAngle = targetAngle;

      /*
      currentAngle = currentAngle + offset;
      double converted_angle = abs(offset * (400/360));
      Serial.print("Target Angle");
      Serial.print(targetAngle);
      Serial.print("Current Angle");
      Serial.print(currentAngle);
      Serial.print(converted_angle);
      converted_angle = int(converted_angle);*/
      
    }
  }
}

void rotateByAngle(int offset) {
  int converted_angle = abs(offset * (400/360));
  for (int i = 0; i < converted_angle ; i++) { // Move 200 steps 200 is 180 deg 400 is 360p
    Serial.print(i);
    digitalWrite(pulsePin, HIGH);
    delayMicroseconds(1000); // Adjust for speed
    digitalWrite(pulsePin, LOW);
    delayMicroseconds(500);
  }
}


bool parseCommand(String command) {
  // Expected format: "ANGLE:<angle>,DIR:<dir>"
  
  if (command.startsWith("ANGLE:")) {
    // Find the comma separator
    int commaIndex = command.indexOf(",");
    if (commaIndex == -1) return false;
    
    // Extract angle value
    String angleStr = command.substring(6, commaIndex);
    
    // Extract throttle value
    if (!command.substring(commaIndex).startsWith(",DIR:")) return false;
    String dirString = command.substring(commaIndex + 5);
    
    // Convert strings to integers
    int angle = angleStr.toInt();
    //char dir = dirString[0];
    currentDir = dirString[0]; 
    // Constrain values to valid ranges
    angle = constrain(angle, 0, 45);
    
    // Update current values
    if (currentDir == 'R') {
    targetAngle = angle;
    } else {
    targetAngle = -angle;
    }

    // EQ: targetAngle = (dir == 'R') ? angle: -angle;
    // currentDir = dir;
       
    return true;
  }
  
  return false;
}
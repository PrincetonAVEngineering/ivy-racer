float currentAngle = 0.0;
char currentDir = 'R';
const int pulsePin = 3;
const int dirPin = 2;

const int STEPS_ONE_REV = 200;
int curr_pos = 0;

int targetAngle = 0;

bool angleThrottleBit = 0;
bool turnDirBit = 0;
bool valueAngleByte[8]; 
bool valueThrottleByte[8]; 

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Send ready message
  Serial.println("Arduino ready!");
  Serial.println("takes in 3 bytes of data representing angle/throttle, direction (counterclockwise/clockwise), value of angle/throttle");

  pinMode(pulsePin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}


void loop() {
  // Check if data is available to read
    // read in 2 bytes

    // first byte followed by second byte
    // first byte
       // first 2 bits: 00 = angle 01 = throttle
       // next bit: 0 = clockwise 1 = counter clockwise
       // next 4 bits = value of angle
    // second byte 
       // first 2 bits: 01 = throttle
       // next 6 bits: value of throttle


    if (Serial.available() >= 2) {
    byte firstByte = Serial.read();
    byte secondByte = Serial.read();

    // Parse first byte
    byte type = (firstByte & 0b11000000) >> 6;  // bits 7-6
    bool direction = (firstByte & 0b00100000) >> 5; // bit 5
    byte angleValue = (firstByte & 0b00011110) >> 1; // bits 4-1 (4-bit value)

    // Parse second byte
    byte throttleType = (secondByte & 0b11000000) >> 6;  // Should be 01
    byte throttleValue = secondByte & 0b00111111; // bits 5-0 (6-bit value)

    if (type == 0b00 && throttleType == 0b01) {
      Serial.print("Angle: ");
      Serial.print(angleValue);
      Serial.print(" | Direction: ");
      Serial.print(direction == 0 ? "Clockwise" : "Counter-clockwise");
      Serial.print(" | Throttle: ");
      Serial.println(throttleValue);
    } else {
      Serial.println("Invalid data format");
    }
  }
}
    
    
    // Parse the received data
    if (parseCommand(data)) {
      // Send acknowledgment with current values
      Serial.print("ACK:ANGLE:");
      Serial.print(targetAngle);
      Serial.print("ACK:DIR:");
      Serial.print(currentDir);

      int offset = abs(targetAngle - currentAngle);

      if (currentDir == 'R') {
         digitalWrite(dirPin, HIGH);    
      }else {
         digitalWrite(dirPin, HIGH);  
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
    char dir = dirString[0];
        
    // Constrain values to valid ranges
    angle = constrain(angle, 0, 45);
    
    // Update current values
    targetAngle = (dir == 'R') ? angle: -angle;
    currentDir = dir;
        
    return true;
  }
  
  return false;
}

const int RF = 8;
const int RB = 9;
const int LF = 10;
const int LB = 11;

void setup() {
  pinMode(RF, OUTPUT);
  pinMode(RB, OUTPUT);
  pinMode(LF, OUTPUT);
  pinMode(LB, OUTPUT);

}

void forward(){
  digitalWrite(RB, LOW);
  digitalWrite(LB, LOW);
  digitalWrite(RF, HIGH);
  digitalWrite(LF, HIGH);
}

void backward(){
  digitalWrite(RF, LOW);
  digitalWrite(LF, LOW);
  digitalWrite(RB, HIGH);
  digitalWrite(LB, HIGH);
}

void halt(){
  digitalWrite(RF, LOW);
  digitalWrite(LF, LOW);
  digitalWrite(RB, LOW);
  digitalWrite(LB, LOW);
}

void forwardRight(){
  digitalWrite(RF, LOW);
  digitalWrite(LF, HIGH);
  digitalWrite(RB, LOW);
  digitalWrite(LB, LOW);
}

void neutralRight(){
  digitalWrite(RF, LOW);
  digitalWrite(LF, HIGH);
  digitalWrite(RB, HIGH);
  digitalWrite(LB, LOW);
}

void backwardRight(){
  digitalWrite(RF, LOW);
  digitalWrite(LF, LOW);
  digitalWrite(RB, HIGH);
  digitalWrite(LB, LOW);
}

void forwardLeft(){
  digitalWrite(RF, HIGH);
  digitalWrite(LF, LOW);
  digitalWrite(RB, LOW);
  digitalWrite(LB, LOW);
}

void neutralLeft(){
  digitalWrite(RF, HIGH);
  digitalWrite(LF, LOW);
  digitalWrite(RB, LOW);
  digitalWrite(LB, HIGH);
}

void backwardLeft(){
  digitalWrite(RF, LOW);
  digitalWrite(LF, LOW);
  digitalWrite(RB, LOW);
  digitalWrite(LB, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:

}

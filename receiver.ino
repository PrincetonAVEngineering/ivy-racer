/*
* Arduino Wireless Communication Tutorial
*       Example 1 - Receiver Code
*                
* by Dejan Nedelkovski, www.HowToMechatronics.com
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Receiver
RF24 receiver(9, 10); // CE, CSN -- CHANGE LATER

const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  receiver.begin();
  receiver.openReadingPipe(0, address);
  receiver.setPALevel(RF24_PA_MAX);
  receiver.startListening();
}

void loop() {
  if (receiver.available()) {
    char received[13] = "\0";
    receiver.read(&received, sizeof(received));
    Serial.println("Message Received:");
    Serial.println(received);
    // delay(1000);
  }
}

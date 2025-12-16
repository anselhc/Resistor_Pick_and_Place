#include <string.h>

String input = "";

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT); 
  digitalWrite(2, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    if (input == "h") {
      digitalWrite(2, HIGH);
      Serial.print('high');
    }
    if (input == "l") {
      digitalWrite(2, LOW);
      Serial.print('low');
    }
  }
}

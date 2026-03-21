int motorA1 = 7;   // L298N Right motor forward
int motorA2 = 8;   // Right motor backward
int motorB1 = 9;   // Left motor forward
int motorB2 = 10;  // Left motor backward

void setup() {
  Serial.begin(9600);
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
  pinMode(motorB1, OUTPUT);
  pinMode(motorB2, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("Bluetooth Car Ready! Commands: F/B/L/R/S");
}

void stopMotors() {
  digitalWrite(motorA1, LOW);
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, LOW);
  digitalWrite(motorB2, LOW);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    Serial.print("Motor: ");
    
    switch(cmd) {
      case 'F':
        Serial.println("FORWARD");
        digitalWrite(motorA1, HIGH);
        digitalWrite(motorA2, LOW);
        digitalWrite(motorB1, HIGH);
        digitalWrite(motorB2, LOW);
        break;
      case 'B':
        Serial.println("BACKWARD");
        digitalWrite(motorA1, LOW);
        digitalWrite(motorA2, HIGH);
        digitalWrite(motorB1, LOW);
        digitalWrite(motorB2, HIGH);
        break;
      case 'L':
        Serial.println("LEFT");
        digitalWrite(motorA1, HIGH); // Right fwd for left turn
        digitalWrite(motorA2, LOW);
        digitalWrite(motorB1, LOW);
        digitalWrite(motorB2, LOW);
        break;
      case 'R':
        Serial.println("RIGHT");
        digitalWrite(motorA1, LOW);
        digitalWrite(motorA2, LOW);
        digitalWrite(motorB1, HIGH); // Left fwd for right turn
        digitalWrite(motorB2, LOW);
        break;
      case 'S':
        Serial.println("STOP");
        stopMotors();
        digitalWrite(LED_BUILTIN, LOW);
        break;
      default:
        Serial.print("Unknown (");
        Serial.print(cmd);
        Serial.println(")");
    }
    digitalWrite(LED_BUILTIN, HIGH); // Blink LED on any motor command
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
  }
}

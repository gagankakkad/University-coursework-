// Motor A connections
int enA = 9;
int in1 = 8;
int in2 = 7;
// Motor B connections
int enB = 3;
int in3 = 5;
int in4 = 4;
#include "Adafruit_VL53L0X.h"

#define JOYSX1 A0 //defining joysticks and their pins 
#define JOYSY1 A5
#define JOYSX2 4
#define JOYSY2 2
const int swPin = 12;

int State = 0; //x1, y1, x2 and y2
int X1;
int Y1;
int X2;
int Y2;
int switchState = digitalRead(swPin);

Adafruit_VL53L0X lox = Adafruit_VL53L0X();// sensor syntax

void setup() {
  Serial.begin(9600);
  while (! Serial) {
    delay(1);
  }
  Serial.println("Adafruit VL53L0X test");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while (1);
  }
  X1 = (analogRead(JOYSX1)); //simplifies so you dont have to type the whole thing
  Y1 = (analogRead(JOYSY1));
  X2 = (analogRead(JOYSX2));
  Y2 = (analogRead(JOYSY2));

  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(swPin, INPUT);

  // Turn off motors - Initial state
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void loop() {

  if (switchState == HIGH){
  VL53L0X_RangingMeasurementData_t measure;

  Serial.print("Reading a measurement... ");
  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if (measure.RangeStatus != 4) {  // phase failures have incorrect data
    Serial.print("Distance (mm): "); Serial.println(measure.RangeMilliMeter);
  } else {
    Serial.println(" out of range ");
  }

  delay(100);
  if (measure.RangeMilliMeter>=100)//150 mm motor stay on
  {
  directionControlf();
  delay(1000);
  }
  else if (measure.RangeMilliMeter<=100)//150 mm motor stay on
  {
   directionControlb();
   delay(1000);
  }}

  else if (switchState ==LOW){
  Serial.print(" X1 axis: "); // prints the values into the serial monitor
  Serial.println(analogRead(JOYSX1));
  X1 = (analogRead(JOYSX1));
  Serial.println(X1);
  if (X1 >= 800)
  {
    analogWrite(enA, 255);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    delay(500);

  }
  else if ( X1 <= 210)
  {
    analogWrite(enA, 255);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    delay(500);
  }
  Serial.print(" X2 axis: "); // prints the values into the serial monitor
  Serial.println(analogRead(JOYSX2));
  X2 = (analogRead(JOYSX2));
  Serial.println(X2);
  if (X2 >= 2111)
  {
    analogWrite(enB, 255);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(500);

  }
  else if ( X2 <= 210)
  {
    analogWrite(enB, 255);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(500);
  }}
}

// This function lets you control spinning direction of motors
void directionControlf() {
  // Set motors to maximum speed
  // For PWM maximum possible values are 0 to 255
  analogWrite(enA, 255);
  analogWrite(enB, 255);

  // Turn on motor A & B
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  //delay(2000);
}
// Now change motor
void directionControlb() {
  // Set motors to maximum speed
  // For PWM maximum possible values are 0 to 255
  analogWrite(enA, 255);
  analogWrite(enB, 255);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  delay(2000);

}

// This function lets you control speed of the motors

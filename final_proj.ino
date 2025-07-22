#include <AFMotor.h> // Library for Adafruit Motor Shield v1
#include <SoftwareSerial.h> // Library for software serial communication
#include <NewPing.h> // Library for ultrasonic distance sensor
#include <Servo.h> // Library for servo motor control

SoftwareSerial pmsSerial(A4, A5); // Define software serial communication pins

#define MAX_DISTANCE 200 // Maximum distance for ultrasonic sensor
#define MAX_SPEED 100 // Maximum speed for motors
#define MAX_SPEED_OFFSET 20 // Offset for motor speed control

#define TRIG_PIN A0 // Trigger pin for ultrasonic sensor
#define ECHO_PIN A1 // Echo pin for ultrasonic sensor
#define SENS1_PIN A2 // Digital input pin for sensor 1
#define SENS2_PIN A3 // Digital input pin for sensor 2

AF_DCMotor motor1(1); // Define motor 1 (left)
AF_DCMotor motor4(4); // Define motor 4 (right)

boolean goesForward = false; // Flag to track forward movement
int distance = 100; // Variable to store distance from ultrasonic sensor
int speedSet = 0; // Variable to set motor speed

int count = 0; // Counter for number of turns
int pos = 0; // Position variable for servo motor

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE); // Define ultrasonic sensor

Servo myservo; // Define servo motor for scanning
//Servo vac; // Define servo motor for vacuum
//Servo air; // Define servo motor for air control
Servo ESC; // Define servo motor for electronic speed controller

int SENS1_val; // Variable to store sensor 1 value
int SENS2_val; // Variable to store sensor 2 value

void setup() {
  // Initialize pins and servo motors
  pinMode(SENS1_PIN, INPUT);
  pinMode(SENS2_PIN, INPUT);
  myservo.attach(A4);
  myservo.write(115);
 // vac.attach(11);
//  vac.write(45);
 // air.attach(12);
 // air.write(90);
  delay(2000);
  distance = readPing();
  delay(100);
  distance = readPing();
  delay(100);
  distance = readPing();
  delay(100);
  distance = readPing();
  delay(100);
  Serial.begin(115200); // Initialize serial communication
  pmsSerial.begin(9600); // Initialize software serial communication with air quality sensor
  ESC.attach(A5, 1000, 2000); // Attach ESC to pin 13 with min and max pulse widths
}

// Structure to hold data from air quality sensor
struct pms5003data {
  uint16_t framelen;
  uint16_t pm10_standard, pm25_standard, pm100_standard;
  uint16_t pm10_env, pm25_env, pm100_env;
  uint16_t particles_03um, particles_05um, particles_10um, particles_25um, particles_50um, particles_100um;
  uint16_t unused;
  uint16_t checksum;
};

struct pms5003data data;

void loop() {
  int distanceR = 0;
  int distanceL = 0;
  delay(40);

  SENS1_val = digitalRead(SENS1_PIN);
  SENS2_val = digitalRead(SENS2_PIN);

  // Control electronic speed controller

  ESC.write(100);

  // Read data from air quality sensor
  if (readPMSdata(&pmsSerial)) {
    // Print air quality data
    // ... (code to print air quality data)
    delay(1000);
  }

  // Obstacle detection and avoidance
  if (distance <= 20 || SENS1_val == 1 || SENS2_val == 1) {
    moveStop();
    delay(50);
    moveBackward();
    delay(500);
    moveStop();
    delay(200);
    distanceR = lookRight();
    delay(200);
    distanceL = lookLeft();
    delay(200);

    if (distanceR >= distanceL) {
      turnRight();
      moveStop();
      //count = count + 1;
    } else {
      turnLeft();
      moveStop();
      //count = count + 1;
    }
  } else {
    moveForward();
  }

  distance = readPing();
}

// Function to look right and measure distance
int lookRight() {
  myservo.write(50);
  delay(500);
  int distance = readPing();
  delay(100);
  myservo.write(115);
  return distance;
}

// Function to look left and measure distance
int lookLeft() {
  myservo.write(170);
  delay(500);
  int distance = readPing();
  delay(100);
  myservo.write(115);
  return distance;
}

// Function to read distance from ultrasonic sensor
int readPing() {
  delay(70);
  int cm = sonar.ping_cm();
  if (cm == 0) {
    cm = 250;
  }
  return cm;
}

// Function to stop all motors
void moveStop() {
  motor1.run(RELEASE);
  motor4.run(RELEASE);
}

// Function to move forward
void moveForward() {
  if (!goesForward) {
    goesForward = true;
    motor1.run(FORWARD);
    motor4.run(FORWARD);
    for (speedSet = 0; speedSet < MAX_SPEED; speedSet += 2) {
      motor1.setSpeed(speedSet);
      motor4.setSpeed(speedSet);
      delay(5);
    }
  }
}

// Function to move backward
void moveBackward() {
  goesForward = false;
  motor1.run(BACKWARD);
  motor4.run(BACKWARD);
  for (speedSet = 0; speedSet < 190; speedSet += 2) {
    motor1.setSpeed(speedSet);
    motor4.setSpeed(speedSet);
    delay(5);
  }
}

// Function to turn right
void turnRight() {
  motor1.run(FORWARD);
  motor4.run(BACKWARD);
  delay(500);
  motor1.run(FORWARD);
  motor4.run(FORWARD);
}

// Function to turn left
void turnLeft() {
  motor1.run(BACKWARD);
  motor4.run(FORWARD);
  delay(500);
  motor1.run(FORWARD);
  motor4.run(FORWARD);
}

// Function to read data from air quality sensor
boolean readPMSdata(Stream *s) {
  if (!s->available()) {
    return false;
  }

  if (s->peek() != 0x42) {
    s->read();
    return false;
  }

  if (s->available() < 32) {
    return false;
  }

  uint8_t buffer[32];
  uint16_t sum = 0;
  s->readBytes(buffer, 32);

  for (uint8_t i = 0; i < 30; i++) {
    sum += buffer[i];
  }

  uint16_t buffer_u16[15];
  for (uint8_t i = 0; i < 15; i++) {
    buffer_u16[i] = buffer[2 + i * 2 + 1];
    buffer_u16[i] += (buffer[2 + i * 2] << 8);
  }

  memcpy((void *)&data, (void *)buffer_u16, 30);
  if (sum != data.checksum) {
    Serial.println("Checksum failure");
    return false;
  }

  return true;
}

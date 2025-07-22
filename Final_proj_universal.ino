
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <SoftwareSerial.h>

#define CommonSenseMetricSystem
//#define ImperialNonsenseSystem
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define trigPin 9
#define echoPin 10
const int sensorPin = A0;
const int ledPin = 7;
const int ledPin1 = 6;
const byte interruptPin2 = 2;
volatile byte state = LOW;
const byte interruptPin1 = 3;
volatile byte state1 = LOW;
int min_distance = 0;//initial declaration for potentiometer value
int buzzerValue = 12;//declaration for buzzer
const int RX_PIN = 5;
const int TX_PIN = 8;
const int BLUETOOTH_BAUD_RATE = 9600;
SoftwareSerial bluetooth(RX_PIN, TX_PIN);
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
const int RELAY_PIN = 13;

void setup() {
  Serial.begin (9600);
  
  pinMode(ledPin, OUTPUT);
  pinMode (ledPin1, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(interruptPin2, INPUT);
  pinMode(interruptPin1, INPUT);
  bluetooth.begin(9600);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); //initialize with the I2C addr 0x3C (128x64)
  display.clearDisplay();
  pinMode(RELAY_PIN, OUTPUT);

}

void loop() 
{
  long duration, distance;
 // long min_distance;
  min_distance = analogRead(sensorPin); //connecting potentiometer to a value

  min_distance = map(min_distance, 0 , 1023, 0 , 20);
//  min_distance = sensorValue;
  attachInterrupt(digitalPinToInterrupt(interruptPin2), blink, RISING);
  attachInterrupt(digitalPinToInterrupt(interruptPin1), blink1, RISING);
     
  if (state1 == LOW)
  {
   display.setCursor(0,10);  //oled display
  display.setTextSize(1);
  display.setTextColor(WHITE); 
    digitalWrite(ledPin1, HIGH);
    display.println("Car park sensor");
 
    display.println("Press button 1 to activate!");
 
  display.display();
  }
  if (state1 == HIGH)
  {
     digitalWrite(trigPin, LOW);  //PULSE ___|---|___
  delayMicroseconds(2); 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);

    digitalWrite(ledPin1, LOW);
  display.clearDisplay();
  

  
 if (state == LOW)
 {
    distance = (duration/2) * 0.0343;
    display.setCursor(0,10);  //oled display
  display.setTextSize(1);
  display.setTextColor(WHITE);
    display.println ("Minimum distance: ");
  display.print (min_distance);
  display.print(" cm\n");
  display.setTextSize(2);
  display.print(distance);
    display.print(" cm");
    Serial.print("Minimum distance: ");
    Serial.print (min_distance);
  Serial.print(" cm\n");
 // display.setTextSize(2);
 Serial.print ("Distance to obstacle: ");
  Serial.print(distance);
    Serial.println(" cm");

     bluetooth.print ("Minimum distance: ");
  bluetooth.print (min_distance);
  bluetooth.println("cm");
  bluetooth.print ("Distance to Obstacle: ");
  bluetooth.print(distance);
  bluetooth.println("cm");

    
 }
  else if (state == HIGH)
  {
    min_distance = min_distance/2.54;
    distance = (duration/2) / 73.914;
    display.setCursor(0,10);  //oled display
  display.setTextSize(1);
  display.setTextColor(WHITE);
    display.print ("Minimum distance: ");
  display.print (min_distance);
  display.print(" in\n");
  display.setTextSize(2);
  display.print(distance);
    display.print(" in");
    Serial.println ("Minimum distance: ");
    Serial.print (min_distance);
  Serial.print(" in\n");
 // display.setTextSize(2);
 Serial.print ("Distance to obstacle: ");
  Serial.print(distance);
    Serial.println(" in");

     bluetooth.print ("Minimum distance: ");
  bluetooth.print (min_distance);
  bluetooth.println("in");
  bluetooth.print ("Distance to Obstacle: ");
  bluetooth.print(distance);
  bluetooth.println("in");

  }
   if (distance >= min_distance)
  {
    digitalWrite(ledPin, LOW);
  }
  else 
  {
    digitalWrite(ledPin, HIGH);
    tone(buzzerValue, 32.70);
    digitalWrite(RELAY_PIN, HIGH);
  delay(500);
  digitalWrite(RELAY_PIN, LOW);
  delay(500);
  }
  if (distance > min_distance && distance <= (min_distance + 5))
  {
    digitalWrite(ledPin, LOW);
    tone(buzzerValue, 32.70, 200);  
  }
  if (distance > (min_distance + 5) && distance <= (min_distance + 10))
  {
    digitalWrite(ledPin, LOW);
    tone(buzzerValue, 32.70, 100);
    delay (1000);  
  }
  display.display();
 

  }
   delay(500);
  display.clearDisplay();
}
void blink()
{
  state = !state;
  //state1 = !state1;
}
void blink1()
{
  state1 = !state1;
}

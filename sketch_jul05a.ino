#include <Arduino.h>     // every sketch needs this
#include <Wire.h>        // instantiate the Wire library
#include <TFLI2C.h>      // TFLuna-I2C Library v.0.2.0
TFLI2C tflI2C;
int16_t  tfDist;    // distance in centimeters
int16_t  tfAddr = TFL_DEF_ADR;  // use this default I2C address or
                                // set variable to your own value
void setup()
{
    Serial.begin( 115200);  // initialize serial port
    Wire.begin();           // initialize Wire library
    Serial.println( "TFLI2C example code simplified\n"); // say "Hello!"
   // Serial.println( "4 NOV 2021");                     // and add date
}
void loop()
{
    if( tflI2C.getData( tfDist, tfAddr)) // If read okay...
    {
        Serial.print("Dist: cm ");
        unsigned int dist_cm = tfDist*10;
        Serial.println(dist_cm);          // print the data...
        delay(1000);
    }
    else tflI2C.printStatus();           // else, print error.
    delay( 50);
}

#include <AFMotor.h>

AF_DCMotor motor(4);
AF_DCMotor motor1(1);
void setup() 
{
	//Set initial speed of the motor & stop
	motor.setSpeed(200);
	motor.run(RELEASE);
  motor1.setSpeed(200);
	motor1.run(RELEASE);
}

void loop() 
{
	uint8_t i;

	// Turn on motor
	motor.run(FORWARD);
	motor1.run(FORWARD);
	// Accelerate from zero to maximum speed
	for (i=0; i<255; i++) 
	{
		motor.setSpeed(i);  
    motor1.setSpeed(i); 
		delay(10);
	}
	
	// Decelerate from maximum speed to zero
	for (i=255; i!=0; i--) 
	{
		motor.setSpeed(i);  
    motor1.setSpeed(i); 
		delay(10);
	}

	// Now change motor direction
	motor.run(BACKWARD);
  motor1.run(BACKWARD);
	
	// Accelerate from zero to maximum speed
	for (i=0; i<255; i++) 
	{
		motor.setSpeed(i);  
    motor1.setSpeed(i); 
		delay(10);
	}

	// Decelerate from maximum speed to zero
	for (i=255; i!=0; i--) 
	{
		motor.setSpeed(i);  
    motor1.setSpeed(i); 
		delay(10);
	}

	// Now turn off motor
	motor.run(RELEASE);
  motor1.run(RELEASE);
	delay(1000);
}
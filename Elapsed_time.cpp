/* Program to show Elapsed Time oon mbed Application Board LCD Display */

#include "mbed.h"
#include "C12832.h"

C12832 lcd(p5, p7, p6, p8, p11);

volatile int counter = 0, seconds = 0;
volatile int flag = 0;

void led_switch(void);  // Prototypes
void T1_isr(void);

Ticker Tick;
DigitalOut myled(LED1);

void led_switch()        //function blinks led 
{
	myled = !myled;
}

void T1_isr()
/* 1 interrupt every 10 milli sec – so after 100 interrupts increase seconds and set flag */
{
	counter++;
	if (counter >= 100) //1 second has passed?
	{
		seconds++;       // Yes increment seconds
		counter = 0;     // reset counter
		flag = 1;        // set flag to update display
	}
}

int main()
/*initialise ticker with period of 10msec and attach it to T1_isr */
{
	Tick.attach_us(&T1_isr, 10000);   //initializes the ticker with period of 10msec
	//and attaches it to T1 ISR

	lcd.cls();       //clear lcd display
	lcd.locate(0, 0); //show charcters on top left
	lcd.printf("Elapsed Time Monitor");
	while (1) {
		while (flag == 0); // wait for new data
		lcd.locate(0, 15);
		lcd.printf("Elapsed Seconds: %d", seconds);
		flag = 0; //reset flag
		led_switch(); //blink light
	}
}
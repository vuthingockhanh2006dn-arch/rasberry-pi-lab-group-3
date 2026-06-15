from gpiozero import LED
from time import sleep

led = LED(14)

while True:
	led.on()
	sleep(0.05)
	led.off()
	sleep(0.05)

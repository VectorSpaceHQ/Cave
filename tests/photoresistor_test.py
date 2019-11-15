#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
light_PIN = 21

def rc_time (light_PIN):
    count = 0

    #Output on the pin for
    GPIO.setup(light_PIN, GPIO.OUT)
    GPIO.output(light_PIN, GPIO.LOW)
    time.sleep(0.1)
    
    #Change the pin back to input
    GPIO.setup(light_PIN, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(light_PIN) == GPIO.LOW):
        count += 1

    return count

    #Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        light = rc_time(light_PIN)
        if light < 100000:
            print("occupied, {}".format(light))
        else:
            print("unoccupied, {}".format(light))
        
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()


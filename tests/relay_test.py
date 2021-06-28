#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.IN)


while True:
    print("LOW")
    GPIO.output(18, GPIO.LOW)
    time.sleep(3)
    print("HIGH")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3)

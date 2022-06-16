#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

outpin = 19
inpin = 25

GPIO.setup(outpin, GPIO.OUT)
GPIO.setup(inpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    print("LOW")
    GPIO.output(outpin, GPIO.LOW)
    time.sleep(3)
    print("HIGH")
    GPIO.output(outpin, GPIO.HIGH)
    time.sleep(3)

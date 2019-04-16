#!/usr/bin/env python3
# coding: utf-8
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)



def get_motion(PIR_PIN):
    """
    Callback function for PIR sensor
    """
    print("movement detected")
    time.sleep(1)
    

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=get_motion)

while True:
    time.sleep(0.2)
    print("waiting")

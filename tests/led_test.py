#!/usr/bin/env python3
# coding: utf-8
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GREEN_LED = 7
BLUE_LED = 8
RED_LED = 12

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

print("RED")
GPIO.output(RED_LED, True)
time.sleep(1)
GPIO.output(RED_LED, False)

print("GREEN")
GPIO.output(GREEN_LED, True)
time.sleep(1)
GPIO.output(GREEN_LED, False)

print("BLUE")
GPIO.output(BLUE_LED, True)
time.sleep(1)
GPIO.output(BLUE_LED, False)

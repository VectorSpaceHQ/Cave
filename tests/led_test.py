#!/usr/bin/env python3
# coding: utf-8
import RPi.GPIO as GPIO
import time

oGPIO.setmode(GPIO.BCM)

GREEN_LED = 7
BLUE_LED = 8
RED_LED = 12

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

GPIO.output(RED_LED, True)
time.sleep(1)
GPIO.output(RED_LED, False)


GPIO.output(GREEN_LED, True)
time.sleep(1)
GPIO.output(GREEN_LED, False)

GPIO.output(BLUE_LED, True)
time.sleep(1)
GPIO.output(BLUE_LED, False)

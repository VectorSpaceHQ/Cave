#!/usr/bin/env python3
# coding: utf-8
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

MIC_PIN = 22

GPIO.setup(MIC_PIN, GPIO.IN)

while True:
    print(GPIO.input(MIC_PIN))
    time.sleep(0.1)
    

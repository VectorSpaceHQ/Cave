#!/usr/bin/env python3
# coding: utf-8

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class HVAC():
    def __init__(self):
        self.SAFETY_TIMER = 600 # minimum time between state changes, protects compressor
        self.state = "none"
        self.last_state_change = 0
        
        self.getState()
        

    def get_state(self):
        """
        Look at pin states in order to determine hvac state.
        """
        ORANGEPIN = 6
        YELLOWPIN = 13
        GREEN_PIN = 19
        AUX_PIN = 26

        orangeStatus = GPIO.input(ORANGE_PIN)
        yellowStatus = GPIO.input(YELLOW_PIN)
        greenStatus = GPIO.input(GREEN_PIN)
        auxStatus = GPIO.input(AUX_PIN)

        if orangeStatus == 1 and yellowStatus == 1 and greenStatus == 1 and auxStatus == 0:
            self.state = "cool"
            
        elif yellowStatus == 1 and greenStatus == 1:
            if auxStatus == 0:
                self.state = "heat"
            else:
                self.state = "aux heat"

        elif orangeStatus == 0 and yellowStatus == 0 and greenStatus == 0 and auxStatus == 0:
            self.state = "idle"

        elif orangeStatus == 0 and yellowStatus == 0 and greenStatus == 1 and auxStatus == 0:
            self.state = "fan"

        else:
            self.state = "broken"


    def set_state(self, target_state):
        
        self.state = target_state
        
        if time.time() - self.last_state_change > self.SAFETY_TIMER:
            
            self.last_state_change = time.time()
            
            if self.state == "cool":
                GPIO.output(ORANGE_PIN, True)
                GPIO.output(YELLOW_PIN, True)
                GPIO.output(GREEN_PIN, True)
                GPIO.output(AUX_PIN, False)
            elif self.state == "heat":
                GPIO.output(ORANGE_PIN, False)
                GPIO.output(YELLOW_PIN, True)
                GPIO.output(GREEN_PIN, True)
                GPIO.output(AUX_PIN, False)
            elif self.state == "fan":
                GPIO.output(ORANGE_PIN, False)
                GPIO.output(YELLOW_PIN, False)
                GPIO.output(GREEN_PIN, True)
                GPIO.output(AUX_PIN, False)
            elif self.state == "aux":
                GPIO.output(ORANGE_PIN, False)
                GPIO.output(YELLOW_PIN, True)
                GPIO.output(GREEN_PIN, True)
                GPIO.output(AUX_PIN, True)
            elif self.state == "idle":
                GPIO.output(ORANGE_PIN, False)
                GPIO.output(YELLOW_PIN, False)
                GPIO.output(GREEN_PIN, False)
                GPIO.output(AUX_PIN, False)
            else:
                GPIO.output(ORANGE_PIN, False)
                GPIO.output(YELLOW_PIN, False)
                GPIO.output(GREEN_PIN, False)
                GPIO.output(AUX_PIN, False)

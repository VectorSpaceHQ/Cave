#!/usr/bin/env python3
# coding: utf-8

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class HVAC():
    def __init__(self):
        # pin assignments
        self.ORANGE_PIN = 6
        self.YELLOW_PIN = 13
        self.GREEN_PIN = 19
        self.AUX_PIN = 26
        
        self.SAFETY_TIMER = 360 # minimum time between state changes, protects compressor
        self.state = "none"
        self.last_state_change = 0

        GPIO.setup(self.ORANGE_PIN, GPIO.IN)
        GPIO.setup(self.YELLOW_PIN, GPIO.IN)
        GPIO.setup(self.GREEN_PIN, GPIO.IN)
        GPIO.setup(self.AUX_PIN, GPIO.IN)
        
        self.get_state()

        
    def get_state(self):
        """
        Look at pin states in order to determine hvac state.
        """
        orangeStatus = GPIO.input(self.ORANGE_PIN)
        yellowStatus = GPIO.input(self.YELLOW_PIN)
        greenStatus = GPIO.input(self.GREEN_PIN)
        auxStatus = GPIO.input(self.AUX_PIN)

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
        
        if (time.time() - self.last_state_change) > self.SAFETY_TIMER:
            
            self.last_state_change = time.time()
            
            if self.state == "cool":
                GPIO.output(self.ORANGE_PIN, True)
                GPIO.output(self.YELLOW_PIN, True)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
            elif self.state == "heat":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, True)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
            elif self.state == "fan":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, False)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
            elif self.state == "aux":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, True)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, True)
            elif self.state == "idle":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, False)
                GPIO.output(self.GREEN_PIN, False)
                GPIO.output(self.AUX_PIN, False)
            else:
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, False)
                GPIO.output(self.GREEN_PIN, False)
                GPIO.output(self.AUX_PIN, False)


if __name__ == "__main__":
    hvac = HVAC()
    print(hvac.get_state())

#!/usr/bin/env python3
# coding: utf-8

import time
import RPi.GPIO as GPIO
from fysom import FysomGlobalMixin, FysomGlobal

GPIO.setmode(GPIO.BCM)

last_state_change = time.time()


def ready_for_change(e):
    """
    Prevent cycling of the compressor by applying a minimum
    time to wait between state changes.
    """
    SAFETY_TIMER = 20
    if (time.time() - last_state_change) > SAFETY_TIMER:
        return True
    else:
        print("{} seconds until state change allowed".format(
            round(SAFETY_TIMER - (time.time() - last_state_change))))
        return False


    
class HVAC(FysomGlobalMixin):
    GSM = FysomGlobal(
        events=[('cool', 'idle', 'cool'),
                ('heat',  'idle', 'heat'),
                ('fan', 'idle', 'fan'),
                ('idle', ['idle', 'cool', 'heat'], 'idle')],
        callbacks={'on_before_idle': ready_for_change},
        initial='idle',
        state_field='state',
    )
        
    def __init__(self):
        # pin assignments
        self.ORANGE_PIN = 6
        self.YELLOW_PIN = 13
        self.GREEN_PIN = 19
        self.AUX_PIN = 26
        
        self.SAFETY_TIMER = 360 # minimum time between state changes, protects compressor
        self.last_state_change = 0

        GPIO.setup(self.ORANGE_PIN, GPIO.IN)
        GPIO.setup(self.YELLOW_PIN, GPIO.IN)
        GPIO.setup(self.GREEN_PIN, GPIO.IN)
        GPIO.setup(self.AUX_PIN, GPIO.IN)

        self.state = 'idle'
        self.get_state()
        super(HVAC, self).__init__()
        self.onchangestate = self.printstatechange


    def printstatechange(self, e):
        print('change event: {}, src: {}, dst: {}'.format(e.event, e.src, e.dst))
        last_state_change = time.time()

        
    def get_state(self):
        """
        Look at pin states in order to determine true hvac state.
        This is not the software state.
        """
        orangeStatus = GPIO.input(self.ORANGE_PIN)
        yellowStatus = GPIO.input(self.YELLOW_PIN)
        greenStatus = GPIO.input(self.GREEN_PIN)
        auxStatus = GPIO.input(self.AUX_PIN)

        if (orangeStatus == 1 and yellowStatus == 1 and
            greenStatus == 1 and auxStatus == 0):
            self.cool()
            
        elif yellowStatus == 1 and greenStatus == 1:
            if auxStatus == 0:
                self.heat()
            else:
                self.aux()

        elif (orangeStatus == 0 and yellowStatus == 0 and
        greenStatus == 0 and auxStatus == 0):
            self.idle()

        elif (orangeStatus == 0 and yellowStatus == 0 and
        greenStatus == 1 and auxStatus == 0):
            self.fan()

        else:
            self.idle()

        return self.current


    def set_state(self, target_state):
        
        self.state = target_state
        
        if (time.time() - self.last_state_change) > self.SAFETY_TIMER:
            
            self.last_state_change = time.time()
            
            if self.is_state("cool"):
                GPIO.output(self.ORANGE_PIN, True)
                GPIO.output(self.YELLOW_PIN, True)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
            elif self.current == "heat":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, True)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
            elif self.current == "fan":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, False)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
            elif self.current == "aux":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, True)
                GPIO.output(self.GREEN_PIN, True)
                GPIO.output(self.AUX_PIN, True)
            elif self.current == "idle":
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, False)
                GPIO.output(self.GREEN_PIN, False)
                GPIO.output(self.AUX_PIN, False)
            else:
                GPIO.output(self.ORANGE_PIN, False)
                GPIO.output(self.YELLOW_PIN, False)
                GPIO.output(self.GREEN_PIN, False)
                GPIO.output(self.AUX_PIN, False)




def test():
    hvac = HVAC()
    print(hvac.current)
    hvac.cool()
    print(hvac.current)
    hvac.idle()
    print(hvac.current)

    print("physical hvac state: {}".format(hvac.get_state()))    

    
if __name__ == "__main__":
    test()

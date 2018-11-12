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
    SAFETY_TIMER = 200
    if (time.time() - last_state_change) > SAFETY_TIMER:
        print("Changing State")
        return True
    else:
        print("{} seconds until state change allowed".format(
            round(SAFETY_TIMER - (time.time() - last_state_change))))
        print("It has only been {:1.1f} seconds".format(time.time() - last_state_change))
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

        GPIO.setup(self.ORANGE_PIN, GPIO.OUT)
        GPIO.setup(self.YELLOW_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.AUX_PIN, GPIO.OUT)
        
        self.SAFETY_TIMER = 300 # minimum seconds between state changes, protects compressor
        self.last_state_change = 0

        self.state = 'idle'
        super(HVAC, self).__init__()
        self.onchangestate = self.printstatechange


    def printstatechange(self, e):
        print('change from {}, to {}'.format(e.src, e.dst))
        last_state_change = time.time()

        
    def set_state(self, target_state):

        try:
            print("setting state")
            self.state = target_state
        except:
            print("FAILED")

        if (time.time() - self.last_state_change) > self.SAFETY_TIMER:
            print("enough time has passed sinced last state change")
            self.last_state_change = time.time()

            print(self.current)
            
            if self.is_state("cool"):
                print("COOLING")
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
    time.sleep(1)
    if ready_for_change(''):
        hvac.idle()
    else:
        print("not ready")
    print(hvac.current)
    time.sleep(1)
    hvac.cool()
    print(hvac.current)


    
if __name__ == "__main__":
    test()

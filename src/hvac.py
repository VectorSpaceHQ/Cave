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
    SAFETY_TIMER = 500
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
        self.REVERSE_PIN = 20  # reverse
        self.COMPRESSOR_PIN = 21 # compressor
        self.FAN_PIN = 19  # fan
        self.AUX_PIN = 18
        self.GREEN_LED = 7
        self.BLUE_LED = 8
        self.RED_LED = 12
        self.REVERSE_SENSE_PIN = 26
        self.COMPRESSOR_SENSE_PIN = 27
        self.FAN_SENSE_PIN = 25
        self.AUX_SENSE_PIN = 24

        GPIO.setup(self.REVERSE_PIN, GPIO.OUT)
        GPIO.setup(self.COMPRESSOR_PIN, GPIO.OUT)
        GPIO.setup(self.FAN_PIN, GPIO.OUT)
        GPIO.setup(self.AUX_PIN, GPIO.OUT)
        GPIO.setup(self.RED_LED, GPIO.OUT)
        GPIO.setup(self.GREEN_LED, GPIO.OUT)
        GPIO.setup(self.BLUE_LED, GPIO.OUT)

        GPIO.setup(self.REVERSE_SENSE_PIN, GPIO.IN)
        GPIO.setup(self.COMPRESSOR_SENSE_PIN, GPIO.IN)
        GPIO.setup(self.FAN_SENSE_PIN, GPIO.IN)
        GPIO.setup(self.AUX_SENSE_PIN, GPIO.IN)
        
        self.SAFETY_TIMER = 300 # minimum seconds between state changes, protects compressor
        self.last_state_change = 0

        self.state = 'idle'
        super(HVAC, self).__init__()
        self.onchangestate = self.printstatechange


    def printstatechange(self, e):
        print('change from {}, to {}'.format(e.src, e.dst))
        last_state_change = time.time()


    def turn_off(self):
        """
        Used to disable the system in event of errors.
        """
        GPIO.output(self.REVERSE_PIN, False)
        GPIO.output(self.COMPRESSOR_PIN, False)
        GPIO.output(self.FAN_PIN, False)
        GPIO.output(self.AUX_PIN, False)
        GPIO.output(self.BLUE_LED, False)
        GPIO.output(self.RED_LED, False)
        GPIO.output(self.GREEN_LED, False)
                
    def set_state(self, target_state):
        try:
            self.state = target_state
        except:
            print("FAILED to set state")

        if (time.time() - self.last_state_change) > self.SAFETY_TIMER:
            print("enough time has passed sinced last state change")
            self.last_state_change = time.time()

            print("setting state, current state = {}".format(self.current))
            
            if self.is_state("cool"):
                print("COOLING")
                GPIO.output(self.REVERSE_PIN, True)
                GPIO.output(self.COMPRESSOR_PIN, True)
                GPIO.output(self.FAN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
                GPIO.output(self.BLUE_LED, True)
                GPIO.output(self.RED_LED, False)
                GPIO.output(self.GREEN_LED, False)                
            elif self.current == "heat":
                print("HEATING")
                GPIO.output(self.REVERSE_PIN, False)
                GPIO.output(self.COMPRESSOR_PIN, True)
                GPIO.output(self.FAN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
                GPIO.output(self.BLUE_LED, False)
                GPIO.output(self.RED_LED, True)
                GPIO.output(self.GREEN_LED, False)                                
            elif self.current == "fan":
                print("FAN ON")
                GPIO.output(self.REVERSE_PIN, False)
                GPIO.output(self.COMPRESSOR_PIN, False)
                GPIO.output(self.FAN_PIN, True)
                GPIO.output(self.AUX_PIN, False)
                GPIO.output(self.BLUE_LED, True)
                GPIO.output(self.RED_LED, False)
                GPIO.output(self.GREEN_LED, True)                                
            elif self.current == "aux":
                GPIO.output(self.REVERSE_PIN, False)
                GPIO.output(self.COMPRESSOR_PIN, True)
                GPIO.output(self.FAN_PIN, True)
                GPIO.output(self.AUX_PIN, True)
                GPIO.output(self.BLUE_LED, True)
                GPIO.output(self.RED_LED, True)
                GPIO.output(self.GREEN_LED, True)                                
            elif self.current == "idle":
                print("IDLE")
                GPIO.output(self.REVERSE_PIN, False)
                GPIO.output(self.COMPRESSOR_PIN, False)
                GPIO.output(self.FAN_PIN, False)
                GPIO.output(self.AUX_PIN, False)
                GPIO.output(self.BLUE_LED, False)
                GPIO.output(self.RED_LED, False)
                GPIO.output(self.GREEN_LED, False)                                
            else:
                GPIO.output(self.REVERSE_PIN, False)
                GPIO.output(self.COMPRESSOR_PIN, False)
                GPIO.output(self.FAN_PIN, False)
                GPIO.output(self.AUX_PIN, False)
        else:
            remaining = self.SAFETY_TIMER - (time.time() - self.last_state_change)
            print("Safety timer has not expired: {}".format(remaining))


    def get_state(self):
        """
        Check the state of the output pins and determine their true position.
        """
        if GPIO.input(self.FAN_SENSE_PIN):
            print("Fan is on")
        if GPIO.input(self.COMPRESSOR_SENSE_PIN):
            print("Compressor is on")
        if GPIO.input(self.REVERSE_SENSE_PIN):
            print("Reverse flow is on")
        if GPIO.input(self.AUX_SENSE_PIN):
            print("AUX heat is on")

    
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

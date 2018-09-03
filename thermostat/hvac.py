import time

class hvac():
    def __init__(self):
        self.state = "none"
        self.last_state_change = 0
        
        self.getState()
        

    def getState(self):
        """
        Look at pin states in order to determine hvac state.
        """
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)

        ORANGEPIN = 6
        YELLOWPIN = 13
        GREEN_PIN = 19
        AUX_PIN = 26

        orangeStatus = GPIO.input(ORANGE_PIN)
        yellowStatus = GPIO.input(YELLOW_PIN)
        greenStatus = GPIO.input(GREEN_PIN)
        auxStatus = GPIO.input(AUX_PIN)

        old_state = self.state

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


        if old_state <> self.state:
            self.last_state_change = time.time()

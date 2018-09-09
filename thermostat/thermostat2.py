#!/usr/bin/env python3
# coding: utf-8

import database
import error
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class thermostat():
    def __init__(self):
        comfort_offset = 1 # additional offset on top of ASHREA
        PIR_PIN = 20
        
        self.STATUS_LED = 17
        self.target_state = "idle"
        self.active_hysteresis = 1
        self.inactive_hysteresis = 1.5
        self.last_action = 0
        self.motion = 0
        self.comfort_zone = [71 - comfort_offset,
                             76.5 + comfort_offset]

        GPIO.add_event_detect(PIR_PIN, GPIO.RISING,
                              callback=self.get_motion)

        
    def run(self):
        db = database.Database()
        hvac_unit = hvac.HVAC()
        
        while True:
            self.heartbeat()
            
            if (time.time() - self.last_action) > 60: # 60 seconds
                self.get_temperature()
        
                if db.connected:
                    db.store_sensors(self.motion, self.temperature)
                    db.get_targets()
                    self.motion = 0
                else:
                    self.heartbeat()
                    self.fallback_mode()

                hvac_unit.set_state(self.target_state)


    def fallback_mode(self):
        T_min = self.comfort_zone[0]
        T_max = self.comfort_zone[1]

        if hvac_unit.get_state == "idle"
            if self.temperature < (T_min - self.inactive_hysteresis):
                self.target_state = "heat"
            if self.temperature < (T_max + self.inactive_hysteresis):
                self.target_state = "cool"

        else: # Active
            if self.temperature > (T_max + active_hysteresis):
                self.target_state = "idle"
            elif self.temperature < (T_min - active_hysteresis):
                self.target_state = "idle"
                

    def get_temperature():
        """
        Return temperature from a ds18b20 sensor.
        """
        subprocess.Popen('modprobe w1-gpio', shell=True)
        subprocess.Popen('modprobe w1-therm', shell=True)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            error.check_temp(temp_f)

        self.temperature = temp_f
    

    def get_motion(self):
        """
        Callback function for PIR sensor
        """
        self.motion = 1
        

    def set_state(self, target_state):
        hvac.setState(target_state)

    
    def heartbeat(self):
        if GPIO.input(self.STATUS_LED) == True:
            GPIO.output(self.STATUS_LED, False)
        else:
            GPIO.output(self.STATUS_LED, True)


    def log_status(self):
        pass

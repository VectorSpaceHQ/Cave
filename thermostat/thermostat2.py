#!/usr/bin/env python3
# coding: utf-8

import database
import hvac
import error

import subprocess
import RPi.GPIO as GPIO
import time
import datetime
import glob

GPIO.setmode(GPIO.BCM)


class Thermostat():
    def __init__(self):
        comfort_offset = 1 # additional offset on top of ASHREA
        PIR_PIN = 20
        self.LIGHT_PIN = 21
        self.TEMP_PIN = 4
        
        self.STATUS_LED = 17
        self.target_state = "idle"
        self.active_hysteresis = 1
        self.inactive_hysteresis = 1.5
        self.last_action = 0
        self.motion = 0
        self.movement_timeout = 600
        self.last_movement = 0
        self.comfort_zone = [71 - comfort_offset,
                             76.5 + comfort_offset]

        GPIO.setup(self.STATUS_LED, GPIO.OUT)
        GPIO.setup(PIR_PIN, GPIO.IN)
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING,
                              callback=self.get_motion)

        
    def run(self):
        print("initializing db")
        db = database.Database()
        print("initializing hvac")
        self.hvac_unit = hvac.HVAC()
        
        while True:
            self.heartbeat()

            print(self.last_action)
            if (time.time() - self.last_action) > 60: # 60 seconds
                self.reset_sensors()
                self.get_temperature()
        
                if db.connected:
                    db.store_sensors(temp=self.temperature, motion=self.motion, light=self.light)
                    db.get_targets()
                    self.motion = 0
                else:
                    self.heartbeat()
                    self.fallback_mode()

                # self.hvac_unit.set_state(self.target_state)
                
                self.log_status()


    def fallback_mode(self):
        print("Entering Fallback mode")
        print(self.hvac_unit.get_state())
        sys.exit()
        
        T_min = self.comfort_zone[0]
        T_max = self.comfort_zone[1]

        if self.hvac_unit.get_state == "idle":
            if self.temperature < (T_min - self.inactive_hysteresis):
                self.target_state = "heat"
            if self.temperature > (T_max + self.inactive_hysteresis):
                self.target_state = "cool"

        else: # Active
            if self.temperature < (T_max - self.active_hysteresis):
                self.target_state = "idle"
            elif self.temperature > (T_min + self.active_hysteresis):
                self.target_state = "idle"


    def reset_sensors(self):
        if (time.time() - self.last_movement) > self.movement_timeout:
            print("movement has stopped")
            self.motion = 0
            self.light = 0

            
    def get_temperature(self):
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
        self.last_movement = time.time()

        
    def get_light(self):
      count = 0

      #Output on the pin for                                                                 
      GPIO.setup(self.LIGHT_PIN, GPIO.OUT)
      GPIO.output(self.LIGHT_PIN, GPIO.LOW)
      time.sleep(0.1)

      #Change the pin back to input                                                          
      GPIO.setup(self.LIGHT_PIN, GPIO.IN)
        
      #Count until the pin goes high                                                         
      while (GPIO.input(self.LIGHT_PIN) == GPIO.LOW):
          count += 1

      if count < 100000:
          self.light = 1
          self.last_movement = time.time()


    def set_state(self, target_state):
        hvac.setState(target_state)


    def heartbeat(self):
        print("running")
        if GPIO.input(self.STATUS_LED) == True:
            GPIO.output(self.STATUS_LED, False)
        else:
            GPIO.output(self.STATUS_LED, True)


    def log_status(self):
        print("Time: {}, temperature: {}".format(datetime.datetime(), self.temperature))
        print("Target state: {}".format(self.target_state))
        

if __name__ == "__main__":
    thermostat = Thermostat()
    thermostat.run()

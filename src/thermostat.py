#!/usr/bin/env python3
# coding: utf-8

from database import *
import hvac
import error
import os
import subprocess
import configparser
import RPi.GPIO as GPIO
import time
import datetime
import glob

GPIO.setmode(GPIO.BCM)

# db = MySQLDatabase("hvac", host="10.0.0.201", port=3306,
                   # user="vectorspace", passwd="makeheat")


class Thermostat(hvac.HVAC):
    
    def __init__(self):
        super().__init__() # initialize HVAC class

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        config = configparser.ConfigParser()
        config.read(dname+'/config.cfg')

        comfort_offset = float(config['thermostat']['comfort_offset'])
        light_sense = 0
        temp_sense = 0
        ID = 0
        
        PIR_PIN = 20
        self.LIGHT_PIN = 21
        self.TEMP_PIN = 4
        self.ID = 0
        self.location = 'default'

        self.light = 0
        self.humidity = 0
        self.STATUS_LED = 17
        self.target_state = "idle"
        self.active_hysteresis = 1.5
        self.inactive_hysteresis = 1.0
        self.last_action = 0
        self.motion = 0
        self.opmode = 'fallback'
        self.movement_timeout = 600
        self.last_movement = 0
        self.last_beat = time.monotonic()
        self.comfort_zone = [71 - comfort_offset,
                             76.5 + comfort_offset]

        GPIO.setup(self.STATUS_LED, GPIO.OUT)
        GPIO.setup(PIR_PIN, GPIO.IN)
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING,
                              callback=self.get_motion)


        try:
            q = (ModuleInfo
                 .update({ModuleInfo.tempOffset: comfort_offset})
                 .where(ModuleInfo.moduleID == ID))
            q.execute()  # Execute the query.
        except Exception as e:
            print("Warning: no connection to database")

        


    def fallback_mode(self):
        print("Entering Fallback mode")
        self.opmode = 'fallback'
        T_min = self.comfort_zone[0]
        T_max = self.comfort_zone[1]
        self.target_temp = (T_min + T_max) / 2

        if self.current == "idle":
            if self.temperature < (T_min - self.inactive_hysteresis):
                self.target_state = "heat"
                self.target_temp = T_min + self.active_hysteresis
                print("idle, heating, target = {}".format(self.target_temp))
            elif self.temperature > (T_max + self.inactive_hysteresis):
                self.target_state = "cool"
            else:
                print("temperature is in comfort zone")

        else: # Active
            if self.temperature > T_min and self.temperature < (T_max - self.active_hysteresis):
                self.target_state = "idle"
                print("Active and temp is less than tmax - active hysteresis")
                print("active, idling, target = {}".format(self.target_temp))

            elif self.temperature < T_max and self.temperature > (T_min + self.active_hysteresis):
                self.target_state = "idle"
                print("Active and temp is greater than tmin + active hysteresis")

        print("current state: {}, current temp: {}, target temp: {}, target state: {}".format(
            self.current, self.temperature, self.target_temp, self.target_state))
        
    def reset_sensors(self):
        if (time.time() - self.last_movement) > self.movement_timeout:
            self.last_movement = time.time()
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
            temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 2)
            error.check_temp(temp_f)

        self.temperature = temp_f
        return temp_f
    

    def get_motion(self, PIR_PIN):
        """
        Callback function for PIR sensor
        """
        print("movement detected")
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
      while (GPIO.input(self.LIGHT_PIN) == GPIO.LOW) and count < 100000:
          count += 1

      print("light value = ", count)
      if count < 4000:
          self.light = 1
          self.last_movement = time.time()


    def heartbeat(self):
        if time.monotonic() - self.last_beat > 4:
            if self.opmode == 'smart':
                print("smart opmode")
                GPIO.output(self.STATUS_LED, True)
                time.sleep(1)
                GPIO.output(self.STATUS_LED, False)
            elif self.opmode == 'fallback':
                print("fallback opmode")
                for i in range(3):
                    GPIO.output(self.STATUS_LED, True)
                    time.sleep(0.2)
                    GPIO.output(self.STATUS_LED, False)
                    time.sleep(0.1)
            self.last_beat = time.monotonic()

            
    def log_status(self):
        print("Time: {}, temperature: {}".format(datetime.datetime.now(), self.temperature))
        print("Current State: {}, Target state: {}".format(self.current, self.target_state))
        print("Comfort Zone: {}".format(self.comfort_zone))

        try:
            ThermostatLog.create(moduleID = self.ID,
                                 actualTemp = round(self.temperature,1),
                                 state = self.current,
                                 coolOn = 0,
                                 heatOn = 0,
                                 fanOn = 0,
                                 auxOn = 0)
        except:
            print("No connection to DB. Skipping log")
        
    def run(self):
        while True:
            self.heartbeat()

            if (time.time() - self.last_action) > 60: # 60 seconds
                self.last_action = time.time()
                self.reset_sensors()
                self.get_temperature()
                self.get_light()

                try:
                    db.connect(reuse_if_open=True)
                    SensorData.create(moduleID = self.ID,
                                      location = self.location,
                                      state = self.current,
                                      temperature = round(self.temperature, 1),
                                      humidity = self.humidity,
                                      motion = self.motion,
                                      light = self.light)
                    print("sensor data added to DB")

                    last_record = ThermostatSet.select().order_by(ThermostatSet.timeStamp.desc()).get()
                    self.target_temp = last_record.targetTemp
                    self.target_state = last_record.targetMode
                    print("The target temp is, {}".format(self.target_temp))
                    print("The target state is, {}".format(self.target_state))
                    
                    directive_time = last_record.timeStamp

                    if (datetime.datetime.now() - directive_time).total_seconds() > 360:
                        print("directive has expired, going into fallback mode")
                        self.fallback_mode()
                        
                    self.motion = 0 # reset motion
                    self.opmode = 'smart'
                except Exception as e:
                    print("Smart mode not working:, {}".format(e))
                    self.fallback_mode()

                try:
                    self.set_state(self.target_state)
                except Exception as e:
                    print("WARNING: Couldn't set state")
                    print(e)
                
                self.log_status()
                                      
            time.sleep(3)

            

if __name__ == "__main__":
    thermostat = Thermostat()
    print(thermostat.get_temperature())
    # time.sleep(5)
    try:
        thermostat.run()
    finally:
        hvac_controller = hvac.HVAC()
        hvac_controller.set_state("idle")


#!/usr/bin/env python3
# coding: utf-8

# This program is meant to run on the server. It adds intelligence and
# hopefully efficiency to the system.

from database import *
import os
import configparser
import pyowm
import numpy as np
import time

db = MySQLDatabase("hvac", host="localhost", port=3306,
                   user="vectorspace", passwd="makeheat")


class Server():
    def __init__(self):
        self.T_out = 0
        self.comfort_zone = [71, 76.5]
        self.expire_time = 0
        self.inactive_hysteresis = 1.0
        self.active_hysteresis = 1.5
        self.target_mode = "idle"        

        self.read_config()


    def read_config(self):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        print(abspath, dname)
        os.chdir(dname)
        config = configparser.ConfigParser()
        config.read(dname+"/server.conf")

        self.OUTSIDE_ID = config.get('main','WeatherModuleID')
        self.OWM_APIKEY = config.get('main', 'OWM_APIKey')
        self.LOCATION = config.get('main', 'Location')


    def run(self):
        """
        Read and analyze sensor data in order to modify the comfort zone 
        and target state of the thermostat.
        """
        while True:
            self.read_config()
            self.get_weather()
            self.read_sensors()
            self.analyze_data()
            self.set_targets()
            self.postprocess()
            self.write_database()
            self.write_log()
            
            time.sleep(60)

        
    def get_weather(self):
        """
        Use the OWM library to get the current and future outdoor 
        temperature of your location.

        If outside temperature is more than a degree inside comfort zone, set
        target state to idle and alert owner.
        """
        owm = pyowm.OWM(self.OWM_APIKEY)
        observation = owm.weather_at_id(4771099) # this ID needs to be in config file
        w = observation.get_weather()
        # h = observation.get_humidity()
        self.T_out = w.get_temperature('fahrenheit')['temp']
        # self.H_out = w.get_humidity()
        print("outside temp = " + str(self.T_out))
        
        fc = owm.three_hours_forecast_at_id(4771099)
        f = fc.get_forecast()
        for w in f:
            print(w.get_reference_time(timeformat='iso'), w.get_temperature('fahrenheit')['temp'])



    def read_sensors(self):
        """
        Read in sensor data and thermostat logs
        """
        
        db.connect(reuse_if_open = True)
        self.sensor_data = get_sensor_data()

        self.current_mode = ThermostatLog().select()[-1].state

        # # example implementation
        # motionlist = [x.motion for x in self.sensor_data]
        # print(motionlist)

    
    def current_occupancy(self):
        """
        Determine probability that space is currently occupied.
        First check sensors for light, sound, motion.
        If nothing, look at historical trends.

        self.P_occupancy = 0 - 100%
        """
        motion = [x.motion for x in self.sensor_data[-20:]]
        print(motion)
        self.P_occupancy = 100 * min((motion.count(1)**3) / len(motion), 1) # skew the count. the more counts, the more likely they're real

        print("{}% chance there's someone here".format(self.P_occupancy))


    def future_occupancy(self):
        """
        Calculate the probability of future occupancy and use the building heat
        rate to decide how to modify the current comfort zone.

        pull occupancy data from SystemLog
        create histogram by 30 min intervals
        """
        self.calc_heat_rate()
        
        occ_probabilities = [x.Poccupancy for x in SystemLog.select()] # from systemlog
        bins = np.linspace(0, 1, 10)
        bin_means = (np.histogram(occ_probabilities, bins, weights=data)[0] / np.histogram(data, bins)[0])
        
        print(data[0])
        print(bin_means)

        
    def analyze_data(self):
        """
        Check probability of current occupancy.
        Check probability of future occupancy. If future occupancy is likely
        determine how long is needed in order to heat up/cool down prior to
        occupants arriving
        
        Determine target mode and temp
        """
        
        self.current_occupancy()
        try:
            self.future_occupancy()
        except Exception as e:
            print("WARNING: failed to predict future occupancy")
            print(e)

        # # Probability is n_occupied / 10
        # # Return tuple ((hr, probability), ...)
        # today = datetime.datetime.today().weekday()
        # hours = np.arange(0,23)
        # P_occupied = (0,0)
        # self.pred_time_occupied = 1

        # time_list = [x.timeStamp for x in self.sensor_data]
        # occupancy_list = [x.motion for x in self.sensor_data]

        # for time, occupied in zip(time_list, occupancy_list):
        #     dow = time.weekday()
        #     if today == dow: # Look only at today
        #         hour = time.strftime('%H')
        #         for hr in hours:
        #             if hr == int(hour):
        #                 pass

    def postprocess(self):
        """
        Generate plots and reports.
        """
        pass
    
    def calc_heat_rate(self):
        """
        Return heating and cooling rates based on prior data.
        """
        # time_list, id, target, actual, coolOn, heatOn, fanOn, auxOn = zip(*cooling_data)
        time_list = [x.timeStamp.timestamp() for x in self.sensor_data]
        T_actuals = [x.temperature for x in self.sensor_data]
        self.temperature = T_actuals[0]
        
        dT = np.diff(T_actuals)
        dt = np.diff(time_list)
        dTdt = (dT/dt)*3600

        # Given a dataset of thermostat temperature and an outdoor temperature,
        # Determine how long it typically take to reach target setpoint
        # Calculate heat_rate
        heat_rate = 1 # degree/hr
        
        
    def calc_comfort_zone(self):
        """
        As it becomes less likely that the space is occupied, the comfort zone grows.
        These equations are linear fits of Todd M's table.
        """
        self.comfort_zone = [0.21 * self.P_occupancy + 50,
                             -0.15 * self.P_occupancy + 91.5]
        print("Setting comfort zone based on occupancy")
        print(self.comfort_zone)


    def set_targets(self):
        """
        Use comfort zone to determine target mode and target temp
        """
        
        self.calc_comfort_zone()
        
        T_min = self.comfort_zone[0]
        T_max = self.comfort_zone[1]

        self.target_temp = (T_min + T_max) / 2


        if self.current_mode == "idle":
            if self.temperature < (T_min - self.inactive_hysteresis):
                self.target_mode = "heat"
                self.target_temp = T_min + self.active_hysteresis
            elif self.temperature > (T_max + self.inactive_hysteresis):
                self.target_mode = "cool"
                self.target_temp = T_max - self.active_hysteresis
            else:
                print("Temperature of {:.1f} is in comfort zone".format(self.temperature))

        else: # Active
            if (self.temperature > T_min and
                self.temperature < (T_max - self.active_hysteresis)):
                self.target_mode = "idle"
                print("active and temp is high but less than tmax - active hysteresis")

            elif (self.temperature < T_max and
                  self.temperature > (T_min + self.active_hysteresis)):
                self.target_mode = "idle"
                print("active and temp is low but greater than tmin + active hysteresis")
                
            elif (self.temperature < T_min and
                  self.T_out > (T_min + self.active_hysteresis)
                  or self.temperature > T_max and
                  self.T_out < (T_max - self.active_hysteresis)):
                
                self.target_mode = "idle"
                print("Outside temperature is in your comfort zone. Open the windows!")


    def write_database(self):
        # make entries in the ThermostatSet and SystemLog tables

        # print(0, self.target_temp, self.target_mode, self.expire_time)
        ThermostatSet.create(moduleID = 0,
                             targetTemp = self.target_temp,
                             targetMode = self.target_mode,
                             expiryTime = self.expire_time)
        SystemLog.create(Toutside = self.T_out,
                         lowTarget = self.comfort_zone[0],
                         highTarget = self.comfort_zone[1],
                         Poccupancy = self.P_occupancy)

    
    def write_log(self):
        print("logging")

        
if __name__ == "__main__":
    server = Server()
    server.run()

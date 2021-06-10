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
        self.comfort_zone = [71, 76.5] #ASHRAE
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
        config.read(dname+"/config.cfg")

        self.OUTSIDE_ID = config.get('server','WeatherModuleID')
        self.OWM_APIKEY = config.get('server', 'OWM_APIKey')
        self.LOCATION = config.get('server', 'Location')


    def run(self):
        """
        Read and analyze sensor data in order to modify the comfort zone 
        and target state of the thermostat.
        """
        while True:
            self.read_config()
            try:
                self.get_weather()
            except:
                print("unable to get weather data")
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
        self.radiative_heat = 3 # placeholder for an additive radiation value. Might be able to query this from a RealFeel value
        now = w.get_reference_time(timeformat='iso')
        # self.H_out = w.get_humidity()
        print("outside temp = " + str(self.T_out))
        
        fc = owm.three_hours_forecast_at_id(4771099)
        f = fc.get_forecast()
        for w in f:
            timediff = datetime.datetime.strptime(w.get_reference_time(timeformat='iso'),
                                             "%Y-%m-%d %H:%M:%S+00") - datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S+00")
            future_temp = w.get_temperature('fahrenheit')['temp']

            if timediff.total_seconds() < 15000:
                print("in {}, the outside temperature will be {}".format(timediff, future_temp))
                if future_temp > self.comfort_zone[0] and future_temp < self.comfort_zone[1]:
                    print("outside temperature will be in the comfort zone in {}. Deterimine if we should wait until enabling HVAC.".format(timediff))

            # print(w.get_reference_time(timeformat='iso'), w.get_temperature('fahrenheit')['temp'])



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
        light = [int(x.light) for x in self.sensor_data[-20:]]
        combined = [a or b  for a,b in zip(motion, light)]
        print(motion)
        print(combined)
        self.P_occupancy = 100 * min((combined.count(1)**2) / len(combined), 1) # skew the count. the more counts, the more likely they're real

        print("{}% chance there's someone here".format(self.P_occupancy))


    def future_occupancy(self):
        """
        Calculate the probability of future occupancy and use the building heat
        rate to decide how to modify the current comfort zone.

        pull occupancy data from SystemLog
        create histogram by 30 min intervals

        look at patterns on the same day of week
        look at patterns on same day of month
        look at patterns on same day of year

        Weight these results week > month > year
        """
        self.calc_heat_rate()

        d = datetime.datetime.now()
        current_hour = d.hour
        current_dow = d.weekday()
        current_dom = d.day
        current_doy = d.timetuple().tm_yday
        # print(current_hour, current_dow, current_dom, current_doy)
        
        occ_probabilities = [x.Poccupancy for x in SystemLog.select()] # from systemlog

        dow_data = []
        dom_data = []
        doy_data = []
    
        for x in SystemLog.select():
            timeStamp_unixtime = time.mktime(x.timeStamp.timetuple())
            current_unixtime = time.mktime(datetime.datetime.now().timetuple())
            timediff = timeStamp_unixtime - current_unixtime
            
            if timediff > 0 and timediff < 3600:
                if x.timeStamp.weekday() == current_dow:
                    dow_data.append(x.Poccupancy)
                    print("matches dow ", x.timeStamp)
                if x.timeStamp.day() == current_dom:
                    dom_data.append(x.Poccupancy)
                if x.timeStamp.timetuple().tm_yday == current_doy:
                    doy_data.append(x.Poccupancy)

        if len(dow_data) > 0:
            print("n={} data points indicate a {}% probability of occupancy in the next hour for this day of the week.".format(len(dow_data), dow_data.count(1)/len(dow_data)))
        if len(dom_data) > 0:
            print("n={} data points indicate a {}% probability of occupancy in the next hour for this day of the month.".format(len(dom_data), dom_data.count(1)/len(dom_data)))
        if len(doy_data) > 0:
            print("n={} data points indicate a {}% probability of occupancy in the next hour for this day of the year.".format(len(doy_data), doy_data.count(1)/len(doy_data)))

            
        # bins = np.linspace(0, 1, 10)
        # bin_means = (np.histogram(occ_probabilities, bins)[0] / np.histogram(data, bins)[0])
        # print(bin_means)

        
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
        outside_temps = [x.Toutside for x in SystemLog.select()]


        self.temperature = T_actuals[-1]
        
        dT = np.diff(T_actuals)
        dt = np.diff(time_list)
        dTdt = (dT/dt)*3600
        print(len(outside_temps))
        print(len(dTdt))
        np.polyfit(T_outside, dTdt, 2)

        # Given a dataset of thermostat temperature and an outdoor temperature,
        # Determine how long it typically take to reach target setpoint
        # Calculate heat_rate
        heat_rate = 1 # degree/hr
        
        
    def calc_comfort_zone(self):
        """
        As it becomes less likely that the space is occupied, the comfort zone grows.
        These equations are linear fits of Todd M's table.
        """
        temp_offset = ModuleInfo.get(ModuleInfo.moduleID == 0).tempOffset
        
        self.comfort_zone = [0.21 * self.P_occupancy + 50 - temp_offset,
                             -0.15 * self.P_occupancy + 91.5 + temp_offset]
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
                
            elif ((self.temperature < T_min and
                  self.T_out + self.radiative_heat > T_min)
                  or (self.temperature > T_max and
                  self.T_out + self.radiative_heat < T_max)):
                
                self.target_mode = "idle"
                print("Outside temperature ({}) is in your comfort zone. Open the windows!".format(self.T_out))
                print(self.temperature, T_min, T_max)


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

#!/usr/bin/env python3
# coding: utf-8

# This program is meant to run on the server. It adds intelligence and
# hopefully efficiency to the system.

import database
import os
import configparser

class Server():
    def __init__(self):
        self.T_out = 0
        self.comfort_zone = [71, 76.5]

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
        self.read_config()
        self.get_weather()
        self.read_sensors()
        self.analyze_data()
        self.postprocess()
        self.write_database()
        self.write_log()

        
    def get_weather(self):
        """
        Use the OWM library to get the current and future outdoor 
        temperature of your location.

        If outside temperature is more than a degree inside comfort zone, set
        target state to idle and alert owner.
        """
        owm = pyowm.OWM(OWM_APIKEY)
        observation = owm.weather_at_id(4771099) # this ID needs to be in config file
        w = observation.get_weather()
        # h = observation.get_humidity()
        self.T_out = w.get_temperature('fahrenheit')['temp']
        # self.H_out = w.get_humidity()
        print("outside temp = " + str(self.T_out))


    def read_sensors(self):
        self.sensor_data = database.get_sensor_data()

    
    def determine_occupancy(self):
        """
        Determine probability that space is currently occupied.
        First check sensors for light, sound, motion.
        If nothing, look at historical trends.

        self.P_occupancy = 0 - 100%
        """
        sensor_data = self.read_sensors()
        motion = [x[7] for x in sensor_data[:20]]
        print(motion)
        self.P_occupancy = 100 * min((motion.count(1)**3) / len(motion), 1) # skew the count. the more counts, the more likely they're real
        print("{}% chance there's someone here".format(self.P_occupancy))


    def pred_future_occupancy(self):
        """
        Calculate the probability of future occupancy and use the building heat
        rate to decide how to modify the current comfort zone.

        pull occupancy data from SystemLog
        create histogram by 30 min intervals
        """
        occ_probabilities = [x[4] for x in data] # from systemlog
        bins = np.linspace(0, 1, 10)
        bin_means = (np.histogram(occ_probabilities, bins, weights=data)[0] / np.histogram(data, bins)[0])
        
        print(data[0])
        print(bin_means)

        
    def analyze_data(self):
        id, time_list, z, location, temp, b, c, occupancy_list = zip(*sensor_data)
        self.calc_heat_rate()

        # Probability is n_occupied / 10
        # Return tuple ((hr, probability), ...)
        today = datetime.datetime.today().weekday()
        hours = np.arange(0,23)
        P_occupied = (0,0)
        self.pred_time_occupied = 1

        for time, occupied in zip(time_list, occupancy_list):
            dow = time.weekday()
            if today == dow: # Look only at today
                hour = time.strftime('%H')
                for hr in hours:
                    if hr == int(hour):
                        pass

                    
    def calc_heat_rate(self):
        """
        Return heating and cooling rates based on prior data.
        """
        time_list, id, target, actual, coolOn, heatOn, fanOn, auxOn = zip(*cooling_data)
        time_list = [x.timestamp() for x in time_list]
        dT = np.diff(actual)
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
        self.comfort_zone = [0.21 * self.P_occupancy + 50 - comfort_offset,
                             -0.15 * self.P_occupancy + 91.5 + comfort_offset]
        print("Setting comfort zone based on occupancy")
        print(self.comfort_zone)


    def set_target_mode(self):
        T_min = self.comfort_zone[0]
        T_max = self.comfort_zone[1]

        if self.T_in < T_min:
            self.target_temp = T_min
            if self.T_out > T_min:
                mode = 'idle'
                print("Outside temperature is in your comfort zone. Open the windows!")
            else:
                mode = 'heat'
        elif self.T_in > T_max:
            self.target_temp = T_max
            if self.T_out < T_max:
                mode = 'idle'
                print("The inside temperature is above your comfort zone and the outside temperature is below. Open the windows!")
            else:
               mode = 'cool'
        else:
            print("Temperature is in your comfort zone.")
            print(self.T_in)
            mode = 'idle'

        self.target_mode = mode


    def write_database(self):
        # make entries in the ThermostatSet and SystemLog tables
        pass

    
    def write_log(self):
        print("logging")

        
if __name__ == "__main__":
    server = Server()
    server.run()

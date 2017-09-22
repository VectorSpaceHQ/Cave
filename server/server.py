#!/usr/bin/env python3
# coding: utf-8

import os
import time
import datetime
import sys
import pickle
import numpy as np
import math
import re
import pyowm
import configparser
from PythonDaemon import Daemon
import MySQLdb as mdb
import logging
import paho.mqtt.client as paho


#set working directory to where "autoSetDaemon.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

token = configparser.ConfigParser()
token.read(dname+"/token.txt")

CONN_PARAMS = (token.get('main','mysqlHost'), token.get('main','mysqlUser'),
               token.get('main','mysqlPass'), token.get('main','mysqlDatabase'),
               int(token.get('main','mysqlPort')))

config = configparser.ConfigParser()
config.read(dname+"/server.conf")

T_MIN = float(config.get('main', 'Minimum_Temperature'))
T_MAX = float(config.get('main', 'Maximum_Temperature'))
comfort_zone = [T_MIN, T_MAX]

MYSQL_BACKUP_DIR = config.get('main','mysqlBackupDir')

OUTSIDE_ID = config.get('main','WeatherModuleID')
OWM_APIKEY = config.get('main', 'OWM_APIKey')
LOCATION = config.get('main', 'Location')

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    # timestamp, ID, loc, temp, humidity, light, occupied
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %X')
    moduleID, loc, temp, humid, light, occupied = str(msg.payload)

    conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
    cursor = conDB.cursor()
    cursor.execute("INSERT SensorData SET moduleID={}, location={}, temperature={}, humidity={}, light={}, occupied={}".format(moduleID, loc, temp, humid, light, occupied))
    cursor.close()
    conDB.commit()
    conDB.close()

class autoSetDaemon(Daemon):

    def init_therm_set(self):
        """
        Initialize the thermostatSet table in the MySQL database.
        """
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],
                           CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()

        cursor.execute("SELECT * from ThermostatSet")
        targs = cursor.fetchall()
        if len(targs) == 0:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %X')
            moduleID = 1
            target_temp = 70
            mode = "idle"
            expiry_time = (datetime.datetime.now()+ datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %X')
            print(timestamp, expiry_time)
            entryNo = 1
            cursor.execute("""INSERT ThermostatSet SET moduleID=%s, targetTemp=%s, targetMode='%s', expiryTime='%s', entryNo=1"""%(int(moduleID),int(target_temp),mode,str(expiry_time)))

        cursor.close()
        conn.commit()
        conn.close()
        print("done")

    def get_therm_set(self):
        """
        Return the thermostat setpoint stored in the SQL database.
        """

        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ThermostatSet")
        thermSet = cursor.fetchall()

        cursor.close()
        conn.close()

        if len(thermSet) == 0:
            now = datetime.datetime.now()
            time.sleep(3)
            return [0, 66.0, 0, now]

        return thermSet[0][1:-1]


    def get_sensor_data(self):
        """
        Return sensor data from the SensorData table.
        """
        self.occupied = False

        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SensorData ORDER BY readingID DESC LIMIT 50")
        sensor_data = cursor.fetchall()
        cursor.close()

        if len(sensor_data) == 0:
            print("ERROR: There is no sensor data.")
            print("       Get your thermostat up and running first.")
            sys.exit()

        # Check for occupancy
        # *A, occupancy_list = zip(*sensor_data[:20])
        # for value in occupancy_list:
        #     if value is not None:
        #         self.occupied = True

        self.determine_occupancy(sensor_data)

        last_sensor_time = sensor_data[-1][1]
        self.T_in = float(sensor_data[0][-4])


    def backupDB(self):
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])

        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime('%m-%d-%y-%X')
        timestamp = re.sub(':', '-', timestamp)
        backDir = MYSQL_BACKUP_DIR

        cursor.execute("SELECT * INTO OUTFILE '%s' FROM ThermostatLog"%(os.path.join(backDir,timestamp+'ThermostatLog.csv')))
        conn.commit()

        cursor.execute("SELECT * INTO OUTFILE '%s' FROM SensorData"%(os.path.join(backDir,timestamp+'SensorData.csv')))
        conn.commit()

        cursor.execute("DELETE FROM SensorData WHERE timeStamp < TIMESTAMP(DATE_SUB(NOW(), INTERVAL 35 DAY))")
        conn.commit()

        cursor.execute("DELETE FROM ThermostatLog WHERE timeStamp < TIMESTAMP(DATE_SUB(NOW(), INTERVAL 35 DAY))")
        conn.commit()

        cursor.close()
        conn.close()

        fobj = open('lastBackup.pck','wb')
        pickle.dump(datetime.datetime.now(),fobj)
        fobj.close()


    def get_weather(self):
        """
        Return the next hours temperature based on NOAA predictions.
        """
        # weatherDict = pywapi.get_weather_from_noaa("4771099")
        owm = pyowm.OWM(OWM_APIKEY)
        observation = owm.weather_at_id(4771099)
        w = observation.get_weather()
        # h = observation.get_humidity()
        self.T_out = w.get_temperature('fahrenheit')['temp']
        # self.H_out = w.get_humidity()
        print("outside " + str(self.T_out))
        # print("humidity " + str(self.H_out))

        # fc = owm.three_hours_forecast("4771099")
        # f = fc.get_forecast()
        # for val in f:
        #     print(val)

        # # Store weather as sensor data for outside
        # conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        # cursor = conDB.cursor()
        # cursor.execute("INSERT SensorData SET moduleID=0, location='outside', temperature=%s , humidity =%s" % (str(self.T_out), str(self.H_out))
        # cursor.close()
        # conDB.commit()
        # conDB.close()

        return


    def calc_heat_rate(self):
        """
        Return heating and cooling rates based on prior data.
        """
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ThermostatLog WHERE coolOn = 1")
        cooling_data = cursor.fetchall()
        cursor.close()

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
        These equations are linear fits of Todd's table.
        """
        self.comfort_zone = [0.21 * self.P_occupancy + 50,
                        -0.15 * self.P_occupancy + 91.5]


    def analyze_data(self):
        """
        Calc heating rate
        Calc probability of occupancy
        """
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SensorData")
        sensor_data = cursor.fetchall()
        cursor.close()

        id, time_list, z, location, temp, b, c, occupancy_list = zip(*sensor_data)

        self.calc_heat_rate()
        self.P_occupancy = 100 # Testing

        # Determine the probability that the building will be occupied during
        # each hour of the current day.
        # Look at last 10 occurances of the current day.
        # If at any point during an hour, the space is occupied, then space is occupied for that hour
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

        return


    def determine_occupancy(self, sensor_data):
        """
        Based on sensor data, determine if the space is occupied.
        At least two sensors must agree.
        """
        self.occupied = True # Testing

    def pred_future_occupancy(self):
        """
        Calculate the probability of future occupancy and use the building heat
        rate to decide how to modify the current comfort zone.
        """
        pass


    def mqtt(self):

        client = paho.Client()


    def get_mode(self):
        T_min = self.comfort_zone[0]
        T_max = self.comfort_zone[1]

        if (self.T_in < T_min):
            if self.T_out > T_min:
                mode = 'idle'
                print("Outside temperature is in your comfort zone. Open the windows!")
            else:
                mode = 'heat'
                self.target_temp = T_min
        elif (self.T_in > T_max):
            if self.T_out < T_max:
                mode = 'idle'
                print("Outside temperature is in your comfort zone. Open the windows!")
            else:
               mode = 'cool'
               self.target_temp = T_max
        else:
            print("Temperature is in your comfort zone.")
            print(self.T_in)
            mode = 'idle'

        return mode

    def set_thermostats(self, mode, expTime):
        """
        Update the ThermostatSet table to control thermostats with new directive.
        """

        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()

        cursor.execute("UPDATE ThermostatSet SET moduleID=%s, targetTemp=%s, targetMode='%s', expiryTime='%s' WHERE entryNo=1"
                       %(str(1),str(self.target_temp), mode, str(expTime)))
        conn.commit()

        cursor.close()
        conn.close()


    def run(self, debug=False, plot=False, backup=False):
        """
        Every 60 seconds, get the sensor data, determine if building is occupied,
        look at weather prediction, make decision, direct thermostat on what to do.
        """
        self.init_therm_set()
        while True:
            try:
                curModule, target_temp, mode, expTime = self.get_therm_set()
                old_mode = mode
                curTime = datetime.datetime.now()

                logging.debug("current time: " +str(curTime))
                logging.debug("expTime: " + str(expTime))

                if curTime>expTime:
                    self.get_sensor_data()
                    self.get_weather()
                    self.analyze_data()
                    self.calc_comfort_zone()
                    mode = self.get_mode()

                    # All action changes should have a minimum time of 5 minutes
                    # to prevent oscillations on the compressor.
                    if old_mode != mode:
                        expTime = datetime.datetime.now() + datetime.timedelta(minutes=5)
                    else:
                        expTime = datetime.datetime.now()

                    self.set_thermostats(mode, expTime)


                #########################################
                ##### Check about backups
                #########################################
                try:
                    fobj = open('lastBackup.pck','rb')
                    lastBackup = pickle.load(format())
                    fobj.close()

                    if (curTime-lastBackup).days>30:
                        backup = True
                except:
                    backup = False

                if backup:
                    self.backupDB()

                time.sleep(60)

            except Exception:#IOError:#
                if debug:
                    raise
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                fobj = open(dname+'/logs/autoSetDaemon.log','a')

                fobj.write('Error occurred at %s \n'%(datetime.datetime.now().strftime('%m-%d-%y-%X')))
                fobj.write(str(exc_type.__name__)+'\n')
                fobj.write(str(fname)+'\n')
                fobj.write(str(exc_tb.tb_lineno)+'\n\n')

                time.sleep(5)


if __name__ == "__main__":
    client = paho.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("RPiThermostat/nodes", qos=1)
    client.loop_start()

    daemon = autoSetDaemon(dname+'/autoSetDaemon.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            logging.basicConfig(filename='server.log',level=logging.DEBUG)
            daemon.run(True)
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

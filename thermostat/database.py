#!/usr/bin/env python3
# coding: utf-8
import configparser
import MySQLdb as mdb
import time
import os
from peewee import *


#set working directory to where "server.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

config = configparser.ConfigParser()
config.read(dname+"/token.txt")
CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
        config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
        int(config.get('main','mysqlPort')))


# class Sensor(Model):
#     ID = CharField()

#     class Meta:
#         database = db


class Database():


    def __init__(self):
        self.last_update = 0
        self.connected = False
        # self.update()
        # self.conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])

        
    def connect(self):
        cursor = self.conn.cursor()
        cursor.close()
        conDB.commit()
        conDB.close()

        
    def update(self):
        """
        Continually check connection to database
        """
        while True:
            if (time.time() - self.last_update) > 60:
                self.last_update = time.time()
                try:
                    self.connect()
                    self.connected = True
                except:
                    self.connected = False

                    
    def store_sensors(self, temp="null", motion=0,
                      light="null", humidity="null"):
        self.cursor.execute("INSERT SensorData SET moduleID=1, location='hallway', temperature=%s, motion=%s"%(temp, motion))
        cursor.close()
        conDB.commit()
        conDB.close()

        
    def get_sensor_data(self):
        """
        Return sensor data from the SensorData table.
        """

        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SensorData ORDER BY readingID DESC LIMIT 50")
        sensor_data = cursor.fetchall()
        cursor.close()

        if len(sensor_data) == 0:
            print("ERROR: There is no sensor data.")
            print("       Get your thermostat up and running first.")
            sys.exit()

        last_sensor_time = sensor_data[-1][1]
        self.T_in = float(sensor_data[0][-4])

        return sensor_data


if __name__ == "__main__":
    db = SqliteDatabase('hvac.db')
    
    
            

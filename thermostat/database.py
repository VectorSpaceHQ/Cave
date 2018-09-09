#!/usr/bin/env python3
# coding: utf-8
import configparser
import MySQLdb as mdb

#set working directory to where "server.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

config = configparser.ConfigParser()
config.read(dname+"/token.txt")
CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
        config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
        int(config.get('main','mysqlPort')))

class Database():
    def __init__(self):
        self.last_update = 0
        self.connected = False
        self.update()

        
    def connect(self):
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],
                           CONN_PARAMS[3],port=CONN_PARAMS[4])
        self.cursor = conn.cursor()

        
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

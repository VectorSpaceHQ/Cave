#!/usr/bin/env python3
# coding: utf-8
import configparser
import MySQLdb as mdb
import time
import os
from fysom import FysomGlobalMixin, FysomGlobal

#set working directory to where "server.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

config = configparser.ConfigParser()
config.read(dname+"/token.txt")
CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
        config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
        int(config.get('main','mysqlPort')))


class Database(FysomGlobalMixin):
    GSM = FysomGlobal(
        events=[('cool', 'idle', 'cool'),
                ('heat',  'idle', 'heat'),
                ('fan', 'idle', 'fan'),
                ('idle', ['cool', 'heat'], 'idle')],
        initial='idle',
        state_field='state'
    )
    # GSM = FysomGlobal({ 'initial': 'idle',
    #               'events': [
    #               {'name': 'cool', 'src': 'idle', 'dst': 'cool'},
    #               {'name': 'heat', 'src': 'idle', 'dst': 'heat'},
    #               {'name': 'stop', 'src': ['cool', 'heat'], 'dst': 'idle'},
    #               {'name': 'circulate', 'src': 'idle', 'dst': 'fan'} ] })
    
    def __init__(self):
        self.last_update = 0
        self.connected = False
        # self.update()

        
    def connect(self):
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],
                           CONN_PARAMS[3],port=CONN_PARAMS[4])
        self.cursor = conn.cursor()
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

if __name__ == "__main__":
    db = Database()
    print(db.current)
    
            

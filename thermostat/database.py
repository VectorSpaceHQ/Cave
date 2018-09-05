#!/usr/bin/env python3
# coding: utf-8
import configparser
import MySQLdb as mdb

config = configparser.ConfigParser()
config.read(dname+"/token.txt")
CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
        config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
        int(config.get('main','mysqlPort')))

class database():
    def __init__(self):
        self.connected = False
        self.connect()
        
    def connect(self):
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],
                           CONN_PARAMS[3],port=CONN_PARAMS[4])
        self.cursor = conn.cursor()


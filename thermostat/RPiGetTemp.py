#!/usr/bin/env python3
#Based off the tutorial by adafruit here:
# http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

import subprocess
import glob
import time
import MySQLdb as mdb
import os

import configparser
from . import error

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

config = configparser.ConfigParser()
config.read(dname+"/token.txt")

CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
               config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
               int(config.get('main','mysqlPort')))


def getTemp():
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

        return temp_f



    return read_temp()




if __name__ == "__main__":
    print(getTemp())

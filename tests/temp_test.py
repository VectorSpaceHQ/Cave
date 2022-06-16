#!/usr/bin/env python3
# coding: utf-8
import subprocess
import glob
import sys

subprocess.Popen('modprobe w1-gpio', shell=True)
subprocess.Popen('modprobe w1-therm', shell=True)
try:
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    print("The 1-wire library is successfully enabled")
except:
    print(e)
    print("ERROR: The 1-wire library is not enabled")
    sys.exit()
    

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

print(temp_f)


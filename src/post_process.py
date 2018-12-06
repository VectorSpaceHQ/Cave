#!/usr/bin/env python3
# generate plots from database data

from database import *
import matplotlib.pyplot as plt
# import os
# import configparser
# import matplotlib
import matplotlib.dates as mdates
import numpy as np
from scipy import integrate
import pandas as pd

ndays = 1
db = MySQLDatabase("hvac", host="localhost", port=3306,
                   user="vectorspace", passwd="makeheat")


syslog_time = [x.timeStamp for x in SystemLog.select().where(SystemLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]
T_outside = [x.Toutside for x in SystemLog.select().where(SystemLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]
lowTarget = [x.lowTarget for x in SystemLog.select().where(SystemLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]
highTarget = [x.highTarget for x in SystemLog.select().where(SystemLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]

syslog_time = [x.timeStamp for x in SystemLog.select().where(SystemLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]
P_occupancy = [x.Poccupancy for x in SystemLog.select().where(SystemLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]

state = [x.state for x in ThermostatLog.select().where(ThermostatLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]
thermostat_time = [x.timeStamp for x in ThermostatLog.select().where(ThermostatLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]
T_actual = [x.actualTemp for x in ThermostatLog.select().where(ThermostatLog.timeStamp > datetime.datetime.today() - datetime.timedelta(days=ndays))]


def heat_rate():
    """
    outside temps are on the system time scale while actual room temps are on the thermostat
    timescale. Must be merged using pandas.

    This data should come from a larger dataset
    """
    df1 = pd.DataFrame({'thermostat time':thermostat_time, 'indoor_temp': T_actual,
                        'state':state})
    df2 = pd.DataFrame({'system time':syslog_time, 'outdoor_temp':T_outside })
    df1 = df1.set_index('thermostat time')
    df2 = df2.set_index('system time')
    frames = [df1, df2]

    result = pd.concat(frames, join='outer')
    result = result.interpolate(method='linear', axis=0).ffill().bfill()
    result = result[~result.state.str.contains("idle")]
    heating_results = result.loc[result['state'] == 'heat']
    cooling_results = result.loc[result['state'] == 'cool']
    
    
    shared_time = result.index.values
    indoor_temp = result.indoor_temp.values
    outdoor_temp = result.outdoor_temp.values
    
    dT = np.diff(indoor_temp)
    dt = np.diff(shared_time)
    dt = [float(x)/1E9 for x in dt]

    dTdt = (dT/dt)*3600
    z = np.polyfit(outdoor_temp[:-1], dTdt, 2)
    p = np.poly1d(z)

    xp = np.linspace(0, 100, 100)
    fig, ax1 = plt.subplots(1,1, figsize=(12,8), dpi=80)
    ax1.plot(xp, p(xp), label='heating')
    ax1.legend(loc="upper left")
    ax1.set_ylabel("dT/dt (F/hr)")
    ax1.set_xlabel("Outside Temperature (F)")
    ax1.grid(True)
    ax1.set_title("HVAC Heating Rate")
    plt.savefig("heatrate.png")

    return p, xp
    

def main():
    heat_rate()


    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(16,10), dpi=80, sharex=True)

    ax1.plot(syslog_time, T_outside, 's-', markevery=63, color='purple', label='outside')
    ax1.plot(thermostat_time, T_actual, 'o-', markevery=54, label='inside')
    ax1.fill_between(syslog_time, lowTarget, highTarget, 
                     where=highTarget >= lowTarget, color='grey', alpha=0.5, label='comfort zone')
    ax1.set_xticks(syslog_time)


    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    
    ax1.legend(loc="lower left")
    ax1.set_ylabel("Temperature (F)")
    ax1.set_xlabel("Time")
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%y %H:%m"))
    bool_cool = ['On' if x=='cool' else 'Off' for x in state]
    bool_heat = ['On' if x=='heat' else 'Off' for x in state]
    bool_fan = ['On' if x=='fan' else 'Off' for x in state]
    binary_cool = [1 if x=='cool' else 0 for x in state]
    binary_heat = [1 if x=='heat' else 0 for x in state]
    binary_fan = [1 if x=='fan' else 0 for x in state]
    ax2.plot(thermostat_time, bool_cool, '-s', markevery=57, label='cool')
    ax2.plot(thermostat_time, bool_heat, '-o', markevery=65, label='heat')
    ax2.plot(thermostat_time, bool_fan, '-x', markevery=73, label='fan')

    
    inc_times = [x.timestamp() for x in list(thermostat_time)]

    integrated_cool = integrate.cumtrapz(binary_cool, inc_times, initial=0)
    integrated_fan = integrate.cumtrapz(binary_fan, inc_times, initial=0)
    integrated_heat = integrate.cumtrapz(binary_heat, inc_times, initial=0)

    ax3.plot(thermostat_time, integrated_cool/60, '-s', markevery=57, label='cool')
    ax3.plot(thermostat_time, integrated_heat/60, '-o', markevery=75, label='heat')
    ax3.plot(thermostat_time, integrated_fan/60, '-x', markevery=63, label='fan')
    ax3.legend(loc='best')
    ax3.set_xlabel("Time")
    ax3.set_ylabel("On Time (min)")
    ax3.set_title("Total on Time During Period Shown")


    # ax4.plot(thermostat_time, 100*(integrated_cool/(1E-3+np.array(inc_times)- inc_times[0])),
    #          '-s', markevery=57, label='cool')
    # ax4.plot(thermostat_time, 100*(integrated_heat/(1E-3+np.array(inc_times)- inc_times[0])),
    #          '-o', markevery=75, label='heat')
    # ax4.plot(thermostat_time, 100*(integrated_fan/(1E-3+np.array(inc_times)- inc_times[0])),
    #          '-x', markevery=63, label='fan')
    ax4.plot(thermostat_time, 100*(integrated_cool/(inc_times[-1]- inc_times[0])),
             '-s', markevery=57, label='cool')
    ax4.plot(thermostat_time, 100*(integrated_heat/(inc_times[-1]- inc_times[0])),
             '-o', markevery=75, label='heat')
    ax4.plot(thermostat_time, 100*(integrated_fan/(inc_times[-1]- inc_times[0])),
             '-x', markevery=63, label='fan')
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Percent")
    ax4.legend(loc='best')

    ax2.legend(loc='best')
    ax2.set_xlabel("Time")
    ax2.set_ylabel("On/Off")

    ax1.set_title("Temperature versus time")
    ax2.set_title("Machine State")
    ax4.set_title("Percent of Time On During Period Shown")

    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%y %H:%m"))
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%y %H:%m"))

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)
    plt.suptitle("Thermostat Data, 24-hr period", fontsize=16)
    # plt.show()
    fig.savefig("Thermostat_Report.png", dpi=150)
    

if __name__ == '__main__':
    main()

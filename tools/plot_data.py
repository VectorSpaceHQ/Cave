#!/usr/bin/env python3
import matplotlib.pyplot as plt
import MySQLdb as mdb
import os
import configparser
import matplotlib
import matplotlib.dates as mdates
import numpy as np
from scipy import integrate

#set working directory to where "server.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

token = configparser.ConfigParser()
token.read(dname+"/../thermostat/token.txt")

CONN_PARAMS = (token.get('main','mysqlHost'), token.get('main','mysqlUser'),
        token.get('main','mysqlPass'), token.get('main','mysqlDatabase'),
        int(token.get('main','mysqlPort')))



def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

    
def get_data():
    conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ThermostatLog ORDER BY timeStamp DESC LIMIT 1440")
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM SystemLog ORDER BY timeStamp DESC LIMIT 1440")
    system_data = cursor.fetchall()
    Toutside = [x[1] for x in system_data]
    lowTarget = [x[2] for x in system_data]
    highTarget = [x[3] for x in system_data]
    cursor.close()
    return data, Toutside, lowTarget, highTarget


def main():
    data, Toutside, lowTarget, highTarget = get_data()
    time = [x[0] for x in data]
    T_actual = [x[3] for x in data]
    T_outside = [x[2] for x in data]
    T_target = [x[2] for x in data]
    P_occupancy = [x[4] for x in data]
    cool = [x[4] for x in data]
    heat =[x[5] for x in data]
    fan = [x[6] for x in data]
    aux = [x[7] for x in data]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(16,10), dpi=80)
    ax1.plot(time, T_actual, 'o-', markevery=54, label='inside')
    ax1.fill_between(time, lowTarget, highTarget, 
                     where=highTarget >= lowTarget, color='grey', alpha=0.5, label='comfort zone')
    ax1.plot(time, Toutside, 's-', markevery=63, color='purple', label='outside')
    

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    
    ax1.legend(loc="lower left")
    ax1.set_ylabel("Temperature (F)")
    ax1.set_xlabel("Time")
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%y %H:%m"))
    bool_cool = ['On' if x==1 else 'Off' for x in cool]
    bool_heat = ['On' if x==1 else 'Off' for x in heat]
    bool_fan = ['On' if x==1 else 'Off' for x in fan]
    ax2.plot(time, bool_cool, '-s', markevery=57, label='cool')
    ax2.plot(time, bool_heat, '-o', markevery=65, label='heat')
    ax2.plot(time, bool_fan, '-x', markevery=73, label='fan')
    ax2.plot(time, aux)

    
    inc_times = [x.timestamp() for x in list(reversed(time))]
    integrated_cool = integrate.cumtrapz(cool, inc_times, initial=0)
    integrated_fan = integrate.cumtrapz(fan, inc_times, initial=0)
    integrated_heat = integrate.cumtrapz(heat, inc_times, initial=0)
    ax3.plot(list(reversed(time)), integrated_cool/60, '-s', markevery=57, label='cool')
    ax3.plot(list(reversed(time)), integrated_heat/60, '-o', markevery=75, label='heat')
    ax3.plot(list(reversed(time)), integrated_fan/60, '-x', markevery=63, label='fan')
    ax3.legend(loc='best')
    ax3.set_xlabel("Time")
    ax3.set_ylabel("On Time (min)")
    ax3.set_title("Total on Time During Period Shown")


    ax4.plot(list(reversed(time)), 100*(integrated_cool/(np.array(inc_times)- inc_times[0])),
             '-s', markevery=57, label='cool')
    ax4.plot(list(reversed(time)), 100*(integrated_heat/(np.array(inc_times)- inc_times[0])),
             '-o', markevery=75, label='heat')
    ax4.plot(list(reversed(time)), 100*(integrated_fan/(np.array(inc_times)- inc_times[0])),
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

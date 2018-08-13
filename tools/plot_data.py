#!/usr/bin/env python3
import matplotlib.pyplot as plt
import MySQLdb as mdb
import os
import configparser

#set working directory to where "server.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) + "/../server"
os.chdir(dname)

token = configparser.ConfigParser()
token.read(dname+"/token.txt")

CONN_PARAMS = (token.get('main','mysqlHost'), token.get('main','mysqlUser'),
               token.get('main','mysqlPass'), token.get('main','mysqlDatabase'),
               int(token.get('main','mysqlPort')))


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

    
def get_data():
    conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SystemLog ORDER BY timeStamp DESC LIMIT 1000")
    data = cursor.fetchall()
    cursor.close()
    return data


def main():
    data = get_data()
    time = [x[0] for x in data]
    T_actual = [x[1] for x in data]
    T_outside = [x[2] for x in data]
    T_target = [x[3] for x in data]
    P_occupancy = [x[4] for x in data]

    plt.plot(time, T_actual, label='actual')
    plt.plot(time, T_target, label='target')
    plt.plot(time, T_outside, label='outside')
    plt.legend(loc='auto')
    plt.ylabel("Temperature (F)")
    plt.xlabel("Time")
    plt.save("Temperatures.png")
    

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# coding: utf-8
import configparser
import MySQLdb as mdb
import numpy as np
import os
import datetime
import pandas as pd

    
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
print(abspath, dname)
os.chdir(dname)
token = configparser.ConfigParser()
token.read(dname+"/token.txt")

CONN_PARAMS = (token.get('main','mysqlHost'), token.get('main','mysqlUser'),
               token.get('main','mysqlPass'), token.get('main','mysqlDatabase'),
               int(token.get('main','mysqlPort')))


def integrated_hrs(start, end):
    """
    Calculated integrated hours the compressor has been running
    over the time frame provided.
    """
    conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
    cursor = conDB.cursor()
    queryStr = ("SELECT * FROM ThermostatLog BETWEEN {} AND {}".format(start,end))
    cursor.execute(queryStr)
    states = cursor.fetchall()

    total_time = 0
    for i, state in enumerate(states):
        cool = state[4]
        heat = state[5]

        last_cool = states[i-1][4]
        last_heat = states[i-1][5]

        # start
        if (cool == 1 or heat == 1) and (last_cool == 0 and last_heat == 0):
            start = state[0]

        # end
        if (cool == 0 or heat == 0) and (last_cool == 1 and last_heat == 1):
            end = state[0]
            total_time += end - start

    cursor.close()
    conDB.close()

    return total_time


def pred_future_occupancy():
    """
    Calculate the probability of future occupancy and use the building heat
    rate to decide how to modify the current comfort zone.

    pull occupancy data from SystemLog
    create histogram by 30 min intervals
    """
    conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SystemLog")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    occ_probabilities = [x[4] for x in data]
    bins = np.linspace(0, 1, 10)
    bin_means = (np.histogram(occ_probabilities, bins, weights=data)[0] / np.histogram(data, bins)[0])
    
    print(data[0])
    print(bin_means)



    df = pd.DataFrame(data = {"Time":times, "Value":occ_probabilities})
    df.set_index('Time', inplace=True)
    df = df.groupby([df.index.hour]).mean()
        
    print(df)
          



    # times = [x[0] for x in data]
    # occ_probabilities = [x[4] for x in data]

    # df = pd.DataFrame(data = {"Time":times, "Value":occ_probabilities})
    # df.set_index('Time', inplace=True)
    # print(df)
    # print(pd.__version__)
    # # Taking mean values for a frequency of 2 minutes
    # # times = pd.to_datetime(df.index)
    # # df.groupby(df.index.map(lambda t: t.minute))
    # df.groupby(df.index.to_periods('T'))
    
    # print(df)
    # sys.exit()

    
    # df_group = df.groupby(pd.TimeGrouper(level='Time', freq='Min'))['Value'].agg('mean')
    # df_group.dropna(inplace=True)
    # df_group = df_group.to_frame().reset_index()
    # print(df_group)
    
    # # bins = np.linspace(0, 1, 10)
    # # digitized = np.digitize(occ_probabilities, bins)
    # # bin_means = [occ_probabilities[digitized == i].mean() for i in range(1, len(bins))]
    # # # bin_means = (np.histogram(occ_probabilities, bins, weights=data)[0] / np.histogram(occ_probabilities, bins)[0])
    # # print(digitized)
    # # print(bin_means)
    # sys.exit()

    
pred_future_occupancy()

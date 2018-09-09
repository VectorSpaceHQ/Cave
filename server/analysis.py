#!/usr/bin/env python3
# coding: utf-8


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


    
pred_future_occupancy()

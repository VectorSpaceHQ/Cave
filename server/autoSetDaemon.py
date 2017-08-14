import os
import time
import datetime
import sys
import cPickle as pickle
import numpy as np
import plotly.plotly as plotly

from plotly.graph_objs import *
import plotly.graph_objs as go
import re

import pywapi
import ConfigParser

from PythonDaemon import Daemon

import MySQLdb as mdb

import logging


#set working directory to where "autoSetDaemon.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


config = ConfigParser.ConfigParser()
config.read(dname+"/config.txt")

CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
               config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
               int(config.get('main','mysqlPort')))

MYSQL_BACKUP_DIR = config.get('main','mysqlBackupDir')


WEB_WEATHER = config.getboolean('main','NOAAWeather')
if WEB_WEATHER:
    WEATHER_ID = config.get('main','NOAACode')

OUTSIDE_ID = config.get('main','WeatherModuleID')



class autoSetDaemon(Daemon):
    def getThermSet(self):
        """
        Return the thermostat setpoint stored in the SQL database.
        """

        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ThermostatSet")
        thermSet = cursor.fetchall()

        cursor.close()
        conn.close()

        if len(thermSet) == 0:
            now = datetime.datetime.now()
            time.sleep(3)
            return [0, 66.0, 0, now]

        return thermSet[0][1:-1]


    def getProgTimes(self,progStr):

        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()

        dayDict = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}

        if progStr == 'Seven Day':
            cursor.execute("SELECT weekDay,time FROM ManualProgram")
            progTimes = cursor.fetchall()
        elif progStr == 'Smart':
            cursor.execute("SELECT weekDay,time FROM SmartProgram")
        else:
            cursor.close()
            return []


        progTimes = [list(pair) for pair in progTimes]
        progDT = []
        for pair in progTimes:
            pair[1] = (datetime.datetime.min + pair[1]).time()
            pair[0] = self.next_weekday(dayDict[pair[0]],pair[1])

            progDT.append(datetime.datetime.combine(pair[0],pair[1]))

        cursor.close()
        conn.close()

        return progDT

    def next_weekday(self, weekday, tod):
        d = datetime.datetime.now()
        days_ahead = weekday - d.date().weekday()

        if days_ahead < 0: # Target day already happened this week
            days_ahead += 7
        if days_ahead == 0:
            if d.time() > tod:
                days_ahead += 7

        return d + datetime.timedelta(days_ahead)


    def backupDB(self):
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])

        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime('%m-%d-%y-%X')
        timestamp = re.sub(':', '-', timestamp)
        backDir = MYSQL_BACKUP_DIR

        cursor.execute("SELECT * INTO OUTFILE '%s' FROM ThermostatLog"%(os.path.join(backDir,timestamp+'ThermostatLog.csv')))
        conn.commit()

        cursor.execute("SELECT * INTO OUTFILE '%s' FROM SensorData"%(os.path.join(backDir,timestamp+'SensorData.csv')))
        conn.commit()

        cursor.execute("DELETE FROM SensorData WHERE timeStamp < TIMESTAMP(DATE_SUB(NOW(), INTERVAL 35 DAY))")
        conn.commit()

        cursor.execute("DELETE FROM ThermostatLog WHERE timeStamp < TIMESTAMP(DATE_SUB(NOW(), INTERVAL 35 DAY))")
        conn.commit()

        cursor.close()
        conn.close()

        fobj = open('lastBackup.pck','wb')
        pickle.dump(datetime.datetime.now(),fobj)
        fobj.close()

    def run(self,debug=False):
        """
        """
        plot = False
        backup = False
        while True:
            try:
                curModule, targTemp, targMode, expTime = self.getThermSet()
                weekList = ['MON','TUE','WED','THU','FRI','SAT','SUN']
                curTime = datetime.datetime.now()

                timeList = self.getProgTimes(actProg)
                logging.debug("time list: " + str(timeList))
                logging.debug("current time: " +str(curTime))
                logging.debug("expTime: " + str(expTime))

                if curTime>expTime:

                    conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
                    cursor = conn.cursor()

                    diffList = [datetime.datetime.now()-timeObj for timeObj in timeList]
                    sortedInds = sorted(range(len(diffList)), key=lambda k: diffList[k])

                    keepInd = [ind for ind in sortedInds if diffList[ind].total_seconds()<0]
                    rowKey = keepInd[0]

                    newExp = timeList[sortedInds[-1]]

                    cursor.execute("SELECT * FROM SmartProgram WHERE rowKey=%s" % (str(rowKey+1)))

                    newData = cursor.fetchall()[0]


                    cursor.execute("UPDATE ThermostatSet SET moduleID=%s, targetTemp=%s, targetMode='%s', expiryTime='%s' WHERE entryNo=1"
                           %(str(newData[3]),str(newData[4]),str(newData[5]),str(newExp)))

                    logging.debug("where: "+str(rowKey+1))
                    logging.debug(newData)

                    conn.commit()
                    cursor.close()
                    conn.close()


                #########################################
                ##### Check about plotting
                #########################################
                try:
                    fobj = open('plotData.pck','rb')
                    lastPlot = pickle.load(fobj)[-1]
                    fobj.close()

                    if (curTime-lastPlot).total_seconds()>600:
                        plot = True
                except:
                    plot = False


                if plot:
                    plotData = self.createPlots(curTime)

                    fobj = open("plotData.pck", "wb")
                    pickle.dump(plotData,fobj)
                    fobj.close()


                #########################################
                ##### Check about backups
                #########################################
                try:
                    fobj = open('lastBackup.pck','rb')
                    lastBackup = pickle.load(format())
                    fobj.close()

                    if (curTime-lastBackup).days>30:
                        backup = True
                except:
                    backup = False

                if backup:
                    self.backupDB()

                time.sleep(60)

            except Exception:#IOError:#
                if debug:
                    raise
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                fobj = open(dname+'/logs/autoSetDaemon.log','a')

                fobj.write('Error occurred at %s \n'%(datetime.datetime.now().strftime('%m-%d-%y-%X')))
                fobj.write(str(exc_type.__name__)+'\n')
                fobj.write(str(fname)+'\n')
                fobj.write(str(exc_tb.tb_lineno)+'\n\n')

                time.sleep(5)


if __name__ == "__main__":
    daemon = autoSetDaemon(dname+'/autoSetDaemon.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            logging.basicConfig(filename='thermostat2.log',level=logging.DEBUG)
            daemon.run(True)
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

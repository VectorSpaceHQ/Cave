#!/usr/bin/env python3
import sys
import subprocess
import os
import time
import RPi.GPIO as GPIO
import datetime
import configparser

import MySQLdb as mdb

from PythonDaemon import Daemon

from RPiGetTemp import getTemp

#set working directory to where "thermDaemonDB.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
# os.chdir(dname)

#read values from the config file
config = configparser.ConfigParser()
config.read(dname+"/thermostat.conf")

active_hysteresis = float(config.get('main','active_hysteresis'))
inactive_hysteresis = float(config.get('main','inactive_hysteresis'))


ORANGE_PIN = int(config.get('main','ORANGE_PIN'))
YELLOW_PIN = int(config.get('main','YELLOW_PIN'))
GREEN_PIN = int(config.get('main','GREEN_PIN'))
AUX_PIN = int(config.get('main','AUX_PIN'))
PIR_PIN = int(config.get('main','PIR_PIN'))
TEMP_PIN = int(config.get('main','TEMP_PIN'))

AUX_ID = int(config.get('main','AUX_ID'))

AUX_TIMER = 10 #minutes
AUX_THRESH = 0.2 #degrees

config = configparser.ConfigParser()
config.read(dname+"/token.txt")
CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
        config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
        int(config.get('main','mysqlPort')))


class thermDaemon(Daemon):

    def configureGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ORANGE_PIN, GPIO.OUT)
        GPIO.setup(YELLOW_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.setup(AUX_PIN, GPIO.OUT)

        GPIO.setup(PIR_PIN, GPIO.IN)
        GPIO.setup(TEMP_PIN, GPIO.IN)

        subprocess.Popen("echo " + str(ORANGE_PIN) + " > /sys/class/gpio/export", shell=True)
        subprocess.Popen("echo " + str(YELLOW_PIN) + " > /sys/class/gpio/export", shell=True)
        subprocess.Popen("echo " + str(GREEN_PIN) + " > /sys/class/gpio/export", shell=True)
        subprocess.Popen("echo " + str(AUX_PIN) + " > /sys/class/gpio/export", shell=True)

    def getHVACState(self):
        """
        orange: reverse airflow (cool)
        yellow: compressor
        green: fan
        aux:

        Return a 4 value tuple.
        (0, 0, 0, 0) : idle
        elif hvacState == (1,0,1,0) or hvacState == (1,0,1,1) heating
        elif hvacState == (1,1,0,0): # it's cold out, why is the AC running?
        """
        orangeStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(ORANGE_PIN) + "/value", shell=True, stdout=subprocess.PIPE).stdout.read().strip())
        yellowStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(YELLOW_PIN) + "/value", shell=True, stdout=subprocess.PIPE).stdout.read().strip())
        greenStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(GREEN_PIN) + "/value", shell=True, stdout=subprocess.PIPE).stdout.read().strip())
        auxStatus = int(subprocess.Popen("cat /sys/class/gpio/gpio" + str(AUX_PIN) + "/value", shell=True, stdout=subprocess.PIPE).stdout.read().strip())


        if orangeStatus == 1 and yellowStatus == 1 and greenStatus == 1 and auxStatus == 0:
          #cooling
            return (1, 1, 0, 0)

        elif yellowStatus == 1 and greenStatus == 1:
             #heating
            if auxStatus == 0:
                return (1, 0, 1, 0)
            else:
                return (1, 0, 1, 1)

        elif orangeStatus == 0 and yellowStatus == 0 and greenStatus == 0 and auxStatus == 0:
            #idle
            return (0, 0, 0, 0)

        elif orangeStatus == 0 and yellowStatus == 0 and greenStatus == 1 and auxStatus == 0:
            #fan
            return (1, 0 , 0, 0)

        else:
            #broken
            return (1, 1, 1, 1)

    def cool(self):
        GPIO.output(ORANGE_PIN, True)
        GPIO.output(YELLOW_PIN, True)
        GPIO.output(GREEN_PIN, True)
        GPIO.output(AUX_PIN, False)
        return (1, 1, 0, 0)

    def heat(self):
        GPIO.output(ORANGE_PIN, False)
        GPIO.output(YELLOW_PIN, True)
        GPIO.output(GREEN_PIN, True)
        GPIO.output(AUX_PIN, False)
        return (1, 0, 1, 0)

    def aux(self):
        GPIO.output(ORANGE_PIN, False)
        GPIO.output(YELLOW_PIN, True)
        GPIO.output(GREEN_PIN, True)
        GPIO.output(AUX_PIN, True)
        return (1, 0, 1, 1)

    def fan(self):
        #to blow the rest of the heated / cooled air out of the system
        GPIO.output(ORANGE_PIN, False)
        GPIO.output(YELLOW_PIN, False)
        GPIO.output(GREEN_PIN, True)
        GPIO.output(AUX_PIN, False)
        return (1, 0, 0, 0)

    def idle(self):
        GPIO.output(ORANGE_PIN, False)
        GPIO.output(YELLOW_PIN, False)
        GPIO.output(GREEN_PIN, False)
        GPIO.output(AUX_PIN, False)
        #delay to preserve compressor
        print('Idling...')
        time.sleep(360)
        return (0, 0, 0, 0)

    def off(self):
        GPIO.output(ORANGE_PIN, False)
        GPIO.output(YELLOW_PIN, False)
        GPIO.output(GREEN_PIN, False)
        GPIO.output(AUX_PIN, False)

        return (0, 0, 0, 0)


    
    def getDBTargets(self):
        conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conDB.cursor()

        cursor.execute("SELECT * from ThermostatSet")

        targs = cursor.fetchall()[0]

        cursor.close()
        conDB.close()
        return targs[:-1]


    def getTempList(self):
        """
        Return all temperatures from SensorData table.
        """
        conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conDB.cursor()

        cursor.execute("SELECT MAX(moduleID) FROM ModuleInfo")
        totSensors = int(cursor.fetchall()[0][0])


        allModTemps=[]
        for modID in range(totSensors):
            try:
                queryStr = ("SELECT * FROM SensorData WHERE moduleID=%s ORDER BY readingID DESC LIMIT 1" % str(modID+1))
                cursor.execute(queryStr)
                allModTemps.append(float(cursor.fetchall()[0][4]))
            except:
                pass

        cursor.close()
        conDB.close()

        return allModTemps


    def logStatus(self, mode, moduleID, targetTemp,actualTemp,hvacState):
        """
        Log status to the ThermostatLog table.
        """
        conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conDB.cursor()


        cursor.execute("""INSERT ThermostatLog SET mode=%s, moduleID=%s, targetTemp=%s, actualTemp=%s,
                        coolOn=%s, heatOn=%s, fanOn=%s, auxOn=%s"""%
                        (str(mode),str(moduleID),str(targetTemp),str(actualTemp),
                        str(hvacState[1]),str(hvacState[2]),str(hvacState[0]),str(hvacState[3])))

        cursor.close()
        conDB.commit()
        conDB.close()


    def server_mode(self):
        """
        The server is providing directive on what to do.
        """
        setTime, moduleID, targetTemp, target_mode, expiryTime = self.getDBTargets()
        if target_mode == 'heat':
            hvacState = self.heat()
        elif target_mode == 'cool':
            hvacState = self.cool()
        elif target_mode == 'idle':
            hvacState = self.fan()
            time.sleep(30)
            hvacState = self.idle()
        else:
            hvacState = self.idle()
        return hvacState


    def fallback_mode(self, auxBool=False):
        """
        If connection to the server is lost, assume space is occupied and try to
        maintain the comfort zone at all times.
        Set the HVAC unit to cool, heat, aux heat, or idle. Return the state of the HVAC unit.
        """
        hvacState=self.getHVACState()

        T_min = comfort_zone[0]
        T_max = comfort_zone[1]

        if hvacState == (0,0,0,0): #idle
            if tempList[moduleID-1] < (minTemp - inactive_hysteresis):
                hvacState = self.heat()
            if tempList[moduleID-1] < (maxTemp + inactive_hysteresis):
                hvacState = self.cool()

        else: # Active
            if auxBool:
                hvacState = self.aux()
            elif tempList[moduleID-1] > (maxTemp + active_hysteresis):
                self.fan()
                time.sleep(30)
                hvacState = self.idle()
            elif tempList[moduleID-1] < (minTemp - active_hysteresis):
                self.fan()
                time.sleep(30)
                hvacState = self.idle()

        return hvacState


    def run(self,debug=False):
        """
        Every 60 seconds, send the thermostat temperature to the DB.
        Try to ask the server for directions. If the server cannot be reached, operate in a dumb
        mode that simply looks
        Every 5 seconds, set the HVAC state.
        """
        lastDB = time.time()
        lastAux = time.time()
        auxTemp = 0
        auxBool = False
        trueCount = 0
        self.configureGPIO()

        while True:
            try:
                abspath = os.path.abspath(__file__)
                dname = os.path.dirname(abspath)
                os.chdir(dname)

                now = time.time()
                dbElapsed = now - lastDB

                if self.getHVACState()[2] == 1:
                    auxElapsed = now - lastAux
                else:
                    auxElapsed = 0

                print("here")
                setTime, moduleID, targetTemp, targetMode, expiryTime = self.getDBTargets()
                print("done")
                log.debug(setTime, moduleID, targetTemp, targetMode, expiryTime)

                moduleID = int(moduleID)
                targetTemp = int(targetTemp)

                tempList = self.getTempList()

                if auxElapsed > AUX_TIMER*60:

                    curTemp = tempList[AUX_ID-1]
                    delta = float(curTemp)-float(auxTemp)
                    auxTemp = curTemp
                    lastAux = time.time()

                    if delta < AUX_THRESH and self.getHVACState()[2] == 1:
                        trueCount += 1
                        if auxBool is True or trueCount == 3:
                            auxBool = True
                            trueCount = 0
                        else:
                            auxBool = False
                    else:
                        auxBool = False

                if dbElapsed > 60:
                    getTemp(sendToDB=True)
                    self.logStatus(moduleID,targetTemp,tempList[moduleID-1],self.getHVACState())
                    lastDB = time.time()

                # Try to get directive from server. Otherwise operate in dumb mode
                try:
                    self.server_mode()
                except:
                    self.fallback_mode()


                print('Pin Value State:',self.getHVACState())
                print('Target Mode:',targetMode)
                print('Temp from DB:', tempList)
                print('Target Temp:', targetTemp)

                time.sleep(5)

            except Exception as e:
                if debug==True:
                    logging.debug(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

                logging.debug("error occurred at " + str(datetime.datetime.now()))
                logging.debug(fname)
                return


if __name__ == "__main__":
    daemon = thermDaemon(dname+'/thermDaemon.pid')


    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
#                        daemon.run()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print("restarting")
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            import logging
            logging.basicConfig(filename='thermostat.log',level=logging.DEBUG)
            daemon.run(True)
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

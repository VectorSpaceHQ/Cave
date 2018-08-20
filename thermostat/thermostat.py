#!/usr/bin/env python3
# coding: utf-8
import sys
import subprocess
import os
import time
import RPi.GPIO as GPIO
import datetime
import configparser
import MySQLdb as mdb
import logging

# local imports. Can't figure out how this should actually be done
try:
    from thermostat.PythonDaemon import Daemon
except:
    from PythonDaemon import Daemon
try:
    from thermostat import RPiGetTemp
except:
    import RPiGetTemp
try:
    from thermostat import error
except:
    import error


#set working directory to where "thermDaemonDB.py" is
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
# os.chdir(dname)

#read values from the config file
config = configparser.ConfigParser()
config.read(dname+"/thermostat.conf")

active_hysteresis = 1
inactive_hysteresis = 1.5
ORANGE_PIN = 6
YELLOW_PIN = 13
GREEN_PIN = 19
AUX_PIN = 26
PIR_PIN = 20
TEMP_PIN = 4
AUX_ID = 1

AUX_TIMER = 10 #minutes
AUX_THRESH = 0.2 #degrees

config = configparser.ConfigParser()
config.read(dname+"/token.txt")
CONN_PARAMS = (config.get('main','mysqlHost'), config.get('main','mysqlUser'),
        config.get('main','mysqlPass'), config.get('main','mysqlDatabase'),
        int(config.get('main','mysqlPort')))



class thermDaemon(Daemon):
    def init_module_info(self):
        """
        If the ModuleInfo table is empty, this function will populate it with default values.
        This table is required before any other tables can be populated.
        """
        conn = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],
                           CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conn.cursor()

        cursor.execute("SELECT * from ModuleInfo")
        targs = cursor.fetchall()
        if len(targs) == 0:
            cursor.execute("""INSERT ModuleInfo SET strDescription='thermostat', FirmwareVer='1', tempSense=1, humiditySense=0, lightSense=0, motionSense=1""")

        cursor.close()
        conn.commit()
        conn.close()

    def getMotion(self, PIR_PIN):
        print("MOVEMENT DETECTED")
        self.occupied = 1
        self.motion = 1
        self.last_movement = time.time()

    def configureGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ORANGE_PIN, GPIO.OUT)
        GPIO.setup(YELLOW_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.setup(AUX_PIN, GPIO.OUT)

        GPIO.setup(PIR_PIN, GPIO.IN)
        GPIO.setup(TEMP_PIN, GPIO.IN)
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=self.getMotion)

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
        (coolOn, heatOn, fanOn, auxOn)
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
        time.sleep(3)
        # time.sleep(360)
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
        targs = cursor.fetchall()

        if len(targs) == 0:
            print("ERROR: database is empty. Execute server.py to initialize")
            sys.exit()

        cursor.close()
        conDB.close()
        return targs[0][:-1]


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


    def logStatus(self, moduleID, targetTemp,actualTemp,hvacState):
        """
        Log status to the ThermostatLog table.
        """
        conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conDB.cursor()


        cursor.execute("""INSERT ThermostatLog SET moduleID=%s, targetTemp=%s, actualTemp=%s,
                        coolOn=%s, heatOn=%s, fanOn=%s, auxOn=%s"""%
                        (str(moduleID),str(targetTemp),str(actualTemp),
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



    def report_sensor_data(self):
        """
        Get temperature, humidity, light, and motion sensor readings.
        Send them to the SensorData table in the server's database.
        """
        print("Reporting sensor data")
        temp_f = "NULL"
        humidity = "NULL"
        light = "NULL"

        temp_f = RPiGetTemp.getTemp()

        conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
        cursor = conDB.cursor()
        cursor.execute("INSERT SensorData SET moduleID=1, location='hallway', temperature=%s, motion=%s"%(str(temp_f), int(self.motion)))
        cursor.close()
        conDB.commit()
        conDB.close()


    def run(self,debug=False):
        """
        Every 60 seconds, send the thermostat temperature to the server's DB.
        Try to ask the server for directions. If the server cannot be reached, operate in a dumb
        mode that simply looks
        Every 5 seconds, set the HVAC state.
        """
        lastDB = time.time()
        lastAux = time.time()
        auxTemp = 0
        auxBool = False
        trueCount = 0
        movement_timeout = 60 # small only for debugging
        self.occupied = 0
        self.last_movement = time.time()
        self.init_module_info()
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

                setTime, moduleID, targetTemp, targetMode, expiryTime = self.getDBTargets()

                moduleID = int(moduleID)
                targetTemp = int(targetTemp)

                tempList = self.getTempList()

                if (time.time() - self.last_movement) > movement_timeout:
                    print("movement has stopped")
                    self.occupied = 0
                    self.motion = 0

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

                print("dbElapsed = " +str(dbElapsed))
                if dbElapsed > 60:
                    self.report_sensor_data()
                    self.logStatus(moduleID, targetTemp, tempList[moduleID-1], self.getHVACState())
                    lastDB = time.time()

                # Try to get directive from server. Otherwise operate in fallback mode
                try:
                    print("server mode")
                    self.server_mode()
                except:
                    msg = "Operating in fallback mode"
                    print(msg)
                    error.notify_email(msg)
                    self.fallback_mode()


                print('Pin Value State:',self.getHVACState())
                print('Target Mode:',targetMode)
                print('Temp from DB:', tempList)
                print('Target Temp:', targetTemp)

                time.sleep(5)

            except Exception as e:
                if debug==True:
                    print(e)
                self.idle()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

                logging.debug("error occurred at " + str(datetime.datetime.now()))
                logging.debug(fname)
                return


if __name__ == "__main__":
    daemon = thermDaemon(dname+'/thermDaemon.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.run()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print("restarting")
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            logging.basicConfig(filename='thermostat.log',level=logging.DEBUG)
            daemon.run(True)
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

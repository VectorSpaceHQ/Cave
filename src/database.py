#!/usr/bin/env python3
# coding: utf-8
import datetime
from peewee import *

db = MySQLDatabase("hvac", host="localhost", port=3306, user="vectorspace", passwd="makeheat")


def get_sensor_data():
    # for entry in SensorData.select():
    #     print(entry.motion)
        
    return SensorData.select()


class newtable(Model):
    Temperature = FloatField()
    class Meta:
        database = db

        
class ModuleInfo(Model):
    moduleID = IntegerField()
    description = CharField()
    firmwareVer = CharField()
    tempSense = IntegerField()
    humiditySense = IntegerField()
    lightSense = IntegerField()
    motionSense = IntegerField()

    class Meta:
        database = db
        
class SensorData(Model):
    readingID = IntegerField()
    timeStamp = DateTimeField(default=datetime.datetime.now)
    moduleID = IntegerField()
    location = CharField()
    temperature = FloatField()
    humidity = FloatField()
    light = FloatField()
    motion = IntegerField()

    class Meta:
        database = db

class SystemLog(Model):
    timeStamp = DateTimeField(default=datetime.datetime.now)
    Toutside = FloatField()
    lowTarget = FloatField()
    highTarget = FloatField()
    Poccupancy = IntegerField()

    class Meta:
        database = db
        
class ThermostatLog(Model):
    timeStamp = DateTimeField(default=datetime.datetime.now)
    moduleID = IntegerField()
    targetTemp = FloatField()
    actualTemp = FloatField()
    state = CharField()
    coolOn = IntegerField()
    heatOn = IntegerField()
    fanOn = IntegerField()
    auxOn = IntegerField()

    class Meta:
        database = db

        
class ThermostatSet(Model):
    timeStamp = DateTimeField(default=datetime.datetime.now)
    moduleID = IntegerField()
    targetTemp = FloatField()
    targetMode = CharField()
    expiryTime = DateTimeField()
    entryNo = PrimaryKeyField()
    
    class Meta:
        database = db

        
if __name__ == "__main__":
    db.connect()
    # if tables don't yet exist, create them
    db.create_tables([SystemLog, ModuleInfo, SensorData, ThermostatSet, ThermostatLog])

    # add rows
    # SystemLog.create(Toutside=50, lowTarget=60, highTarget=80, Poccupancy=1)
    # ThermostatSet.create()
    # ThermostatLog.create()
    # SensorData.create()
    # ModuleInfo.create()
    
    for row in ThermostatLog.select():
        print(row.targetTemp)

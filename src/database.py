#!/usr/bin/env python3
# coding: utf-8
import datetime
from peewee import *


db = MySQLDatabase("hvac", host="10.0.0.201", port=3306, user="vectorspace", passwd="makeheat")


def get_sensor_data():
    # for entry in SensorData.select():
    #     print(entry.motion)
        
    return SensorData.select()


class newtable(Model):
    Temperature = FloatField()
    class Meta:
        database = db

        
class ModuleInfo(Model):
    moduleID = PrimaryKeyField()
    description = CharField()
    firmwareVer = CharField()
    tempSense = IntegerField()
    humiditySense = IntegerField()
    lightSense = IntegerField()
    motionSense = IntegerField()

    class Meta:
        database = db
        
class SensorData(Model):
    readingID = PrimaryKeyField()
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
    actualTemp = FloatField()
    state = CharField()
    coolOn = IntegerField()
    heatOn = IntegerField()
    fanOn = IntegerField()
    auxOn = IntegerField()

    class Meta:
        database = db

        
class ThermostatSet(Model):
    entryNo = PrimaryKeyField()
    timeStamp = DateTimeField(default=datetime.datetime.now)
    moduleID = IntegerField()
    targetTemp = FloatField()
    targetMode = CharField()
    expiryTime = DateTimeField()
    
    class Meta:
        database = db

        
if __name__ == "__main__":
    db.connect()
    # if tables don't yet exist, create them
    db.create_tables([SystemLog, ModuleInfo, SensorData, ThermostatSet, ThermostatLog])

    # Check all tables. If no entries, add one
    if len(SystemLog.select()) == 0:
        SystemLog.create(Toutside=70, lowTarget=60, highTarget=80, Poccupancy=0)
    if len(ModuleInfo.select()) == 0:
        ModuleInfo.create(description="none", firmwareVer=0,
                          tempSense=0, humiditySense=0, lightSense=0, motionSense=0)
    if len(SensorData.select()) == 0:
        SensorData.create(moduleID=0, location="none", temperature=70,
                          humidity=0, light=0, motion=0)
    if len(ThermostatSet.select()) == 0:
        ThermostatSet.create(moduleID=0, targetTemp=70, targetMode="idle",
                             expiryTime=0)
    if len(ThermostatLog.select()) == 0:
        ThermostatLog.create(moduleID=0, actualTemp=70, state="idle",
                             coolOn=0, heatOn=0, fanOn=0, auxOn=0)


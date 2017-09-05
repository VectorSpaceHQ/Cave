An open source, Raspberry Pi based, smart thermostat. Forked from the work done by the Nooganeer (http://www.nooganeer.com/his/).

Overview
=======
This program's goal is to maximize the amount of time spent in the comfort zone while minimizing the energy spent when the building is occupied.


Structure
========
This system is composed of a server, one or more thermostats, and optional nodes.

Server
-------
The server hosts the MySQL database and the web interface. Its purpose is to collect and analyze the sensor data from the thermostat and any additional nodes, and use that information to direct the thermostat(s). In essence, the server is smart. The server can be a dedicated computer or it can run on the Raspberry Pi, alongside the thermostat program.

Thermostat
-------------
The thermostat measures temperature and directly interfaces with the wiring of the HVAC unit. It reports all measurements to the server and its actions are determined by the server. The thermostat is intended to be the Raspberry Pi.

Nodes
------
Nodes are optional pieces of hardware that provide additional sensor data to the MySQL database such as temperatures, humidity, and motion.

Nodes publish data using the MQTT protocol. This is done rather than modifying the MySQL database directly, simply because these nodes are small and rarely support SQL, as in the case of the ESP8266. The RPi subscribes to the MQTT channel and inserts the data it receives into the SQL database.


Installation
===========
clone the repository to the server and thermostat(s).
::
   git clone https://github.com/VectorSpaceHQ/RPiThermostat

Server
-------
Install mysql server on the server.
::
   sudo apt-get install mysql-server

Install supporting packages.
::
   sudo apt-get install python3-dev python3-pip python3-setuptools libmysqlclient-dev

Generate the initial MySQL database.
::
   cd server
   ./generate_sqldb.sh mysqlusername password

Install required python packages.
::
   sudo pip3 install -r ./server/requirements.txt

Install Mosquitto on the server for MQTT brokering.
::
   sudo apt-get install mosquitto

Modify server/token.txt and server/server.conf files with appropriate values based on your wiring and preferences.


Thermostat
-----------
Install required python packages.
::
   sudo pip3 install -r ./thermostat/requirements.txt

Modify thermostat/token.txt and thermostat/thermostat.conf files with appropriate values based on your wiring and preferences.

Enable SPI and 1-Wire.
::
   sudo raspi-config
> Advanced Options > Enable SPI and 1-Wire




Usage
=====
On the server,
::
   ./server/server.py start

On the RPi thermostat run,
::
   ./thermostat/thermostat.py start


MySQL database
=============
The database contains four tables.

ModuleInfo
-----------
This table contains an entry for each module (thermostat or node) connected to the system. It includes a unique ID, a description of the module's location, a firmware version, and boolean values to represent the presence of temperature, humidity, light, and motion sensors.

SensorData
-------------
This table logs all of the sensor readings, including the thermostat(s).

readingID, time, moduleID, location, temperature, humidity, light, occupied

ThermostatLog
-----------------
This table logs only the thermostat readings.

timeStamp, mode, moduleID, targetTemp, actualTemp, coolOn, heatOn, fanOn, auxOn


ThermostatSet
----------------
This table provides the current directive for the thermostat(s). The server writes to this table and the thermostat reads from it.

timeStamp, moduleID, targetTemp, targetMode, expiryTime, entryNo

Testing
======
This software can be tested entirely on a single Raspberry Pi. Install the sample database found in /test, then run both the server.py and thermostat.py programs.
::
    mysql -uroot -p hvac < ./test/hvac_data.txt


Hardware
=======
Below is a wiring diagram for a Raspberry Pi zero with a temperature sensor, PIR sensor, and 4 channel relay.

.. image:: ext/thermostat_schematic_bb.png
           :align: center


HVAC 101
=======
https://github.com/Willseph/RaspberryPiThermostat

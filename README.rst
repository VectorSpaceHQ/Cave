An open source, Raspberry Pi based, smart thermostat. Forked from the work done by the Nooganeer (http://www.nooganeer.com/his/).

Overview
=======
This program's goal is to maximize the amount of time spent in the comfort zone while minimizing the energy spent when the building is occupied.



HVAC 101
=======
https://github.com/Willseph/RaspberryPiThermostat

Modifications
===========
- Removed the concept of modes.
- Replaced plotly with d3, removing reliance of a third party resource to produce plots.
- Written with no regard for python2.

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
clone the repository
git clone https://github.com/VectorSpaceHQ/RPiThermostat

Install mysql server on the server.
.. code:: shell

   sudo apt-get install mysql-server

Install supporting packages.

.. code:: shell
          sudo apt-get install python3-dev libmysqlclient-dev

Generate the initial MySQL database.
./server/generate_sqldb.sh mysqlusername password

Install python packages on the server and thermostat.
sudo pip3 install -r ./server/requirements.txt
sudo pip3 install -r ./thermostat/requirements.txt

Modify the token files with appropriate values.
./thermostat/token.txt
./server/token.txt

Modify the config files with appropriate values based on your wiring and preferences.
./thermostat/thermostat.conf
./server/server.conf

Enable SPI and 1-Wire on the RPi.
sudo raspi-config
Advanced Options
enable SPI and 1-Wire

Install Mosquitto on the server for MQTT brokering.
sudo apt-get install mosquitto


Usage
=====
On the server,
./server/server.py start

On the RPi thermostat run,
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


Warranty
=======
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

An open source, Raspberry Pi based, smart thermostat, forked from the work done by the Nooganeer (http://www.nooganeer.com/his/).

# Overview
This program's goal is to maximize the amount of time spent in the comfort zone while minimizing the energy spent when the building is occupied.

# HVAC 101
https://github.com/Willseph/RaspberryPiThermostat

# Modifications
- Removed the concept of modes.
- Replaced plotly with d3, removing reliance of a third party resource to produce plots.
- Written with no regard for python2.

# ToDO
- Need script to generate initial mysql database.


# Structure
This system is composed of a server, one or more thermostats, and optional nodes.

## Server
The server hosts the MySQL database and the web interface. Its purpose is to collect and analyze the sensor data from the thermostat and any additional nodes, and use that information to direct the thermostat(s). The server can be a dedicated computer or it can run on the Raspberry Pi, alongside the thermostat program.

## Thermostat
The thermostat measures temperature and directly interfaces with the wiring of the HVAC unit. It reports all measurements to the server and its actions are determined by the server. The thermostat is intended to be the Raspberry Pi.

## Nodes
Nodes are optional pieces of hardware that provide additional sensor data to the MySQL database such as temperatures, humidity, and motion.


# Warranty
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

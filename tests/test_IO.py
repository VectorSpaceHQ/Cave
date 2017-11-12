#!/usr/bin/env python3
# coding: utf-8
# Usage: python3 -m unittest discover -t ..
# Mock different temperature readings
# Check pin states to confirm correct behavior
# from tests.context import thermostat
import unittest
import time
from unittest.mock import patch
from unittest.mock import MagicMock
from thermostat.RPiGetTemp import getTemp
import thermostat
import server
from server.server import autoSetDaemon
from thermostat.thermostat import thermDaemon
import os
import threading

def simple_getTemp(temp):
    return temp

class BasicFunction(unittest.TestCase):
    # def test_heat(self):
    #     getTemp = MagicMock(return_value=3)

    #     abspath = os.path.abspath(__file__)
    #     dname = os.path.dirname(abspath)

    #     server_daemon = autoSetDaemon(dname+'/autoSetDaemon.pid')
    #     thermostat_daemon = thermDaemon(dname+'/thermDaemon.pid')
    #     server_daemon.stop()
    #     thermostat_daemon.stop()

    #     server_thread = threading.Thread(target=server_daemon.run)
    #     thermostat_thread = threading.Thread(target=thermostat_daemon.run)
    #     server_thread.start()
    #     thermostat_thread.start()

    #     print("This is a 10 second test of the heating system.")
    #     print("Heating requires the compressor and reverse airflow")
    #     time.sleep(10)
    #     print("DONE")
        
    #     server_daemon.stop()
    #     thermostat_daemon.stop()

        
    def test_cool(self):
        # @patch(RPiGetTemp.getTemp, simple_getTemp)
        getTemp = MagicMock(return_value=100)

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)

        server_daemon = autoSetDaemon(dname+'/autoSetDaemon.pid')
        thermostat_daemon = thermDaemon(dname+'/thermDaemon.pid')

        server_thread = threading.Thread(target=server_daemon.run)
        thermostat_thread = threading.Thread(target=thermostat_daemon.run)
        server_thread.start()
        thermostat_thread.start()

        print("This is a 10 second test of the cooling system.")
        print("Cooling requires the compressor and reverse airflow")
        time.sleep(10)
        server_daemon.stop()
        thermostat_daemon.stop()



if __name__ == '__main__':
    unittest.main()

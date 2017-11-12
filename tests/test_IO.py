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
import thermostat.RPiGetTemp as RPiGetTemp
import thermostat
import server
from server.server import autoSetDaemon
from thermostat.thermostat import thermDaemon
import os

def simple_getTemp(temp):
    return temp

class BasicFunction(unittest.TestCase):
    def test_hot(self):
        # @patch(RPiGetTemp.getTemp, simple_getTemp)
        RPiGetTemp.getTemp = MagicMock(return_value=3)

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)

        
        # server_daemon = autoSetDaemon(dname+'/autoSetDaemon.pid')
        thermostat_daemon = thermDaemon(dname+'/thermDaemon.pid')
        # server_daemon.stop()
        # server_daemon.run()
        thermostat_daemon.stop()
        thermostat_daemon.run()


        
        for i in range(10):
            print("adam")
            time.sleep(1)
        print("DONE")
        daemon.stop()

if __name__ == '__main__':
    unittest.main()

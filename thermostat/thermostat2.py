#!/usr/bin/env python3
# coding: utf-8
import database
import error

class thermostat():
    def __init__(self):
        TEMP_PIN = 4
        STATUS_LED = 17
        active_hysteresis = 1
        inactive_hysteresis = 1.5

    def run(self):
        while True:
            
            time_since_action = time.time() - self.last_action
            
            if time_since_action > 60: # 60 seconds
                self.heartbeat()
                self.read_sensors()
        
                server = database.Server()
                
                if server.connected:
                    self.store_sensors()
                    target_state = self.get_targets()
                else:
                    target_state = self.fallback_mode()
        
                self.set_state(target_state)
        

    def read_sensors(self):
        self.get_motion()
        self.get_temperature()

        
    def get_temperature():
        """
        Return temperature from a ds18b20 sensor.
        """
        subprocess.Popen('modprobe w1-gpio', shell=True)
        subprocess.Popen('modprobe w1-therm', shell=True)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            error.check_temp(temp_f)

        self.temperature = temp_f
    

    def store_sensors(self):
        pass
        
    def get_motion(self):
        PIR_PIN = 20
        print("MOVEMENT DETECTED")
        self.occupied = 1
        self.motion = 1
        self.last_movement = time.time()

    def get_targets(self):
        pass
    
    def set_state(self):
        self.last_action = time.time()


    def set_mode(self):
        pass

    def heartbeat(self):
        pass

    def log_status(self):
        pass

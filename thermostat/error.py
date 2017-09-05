#!/usr/bin/env python3
# Error Handling
#
# In all cases of errors, notify the user by email
# Use LED sequence to display that something is wrong

from gpiozero import RGBLED
import sys
import thermostat

#read values from the config file
config = configparser.ConfigParser()
config.read(dname+"/thermostat.conf")

rgb = config.get('main','RGB_LED')
email = config.get('main', 'email')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_temp(T):
    """
    Check a temperature value for sanity.
    If temp sensor lost, turn off
    If temps ridiculous, turn off
    """
    if not is_number(T):
        e = "Temperature value, {}, is not a number".format(T)
        e += "\nSetting the system to idle mode."
        print(e)
        thermostat.idle()
        notify_email(e)
        sys.exit()

    elif T > 110 or T < -32:
      e ="Temperature value, {}, is out of bounds. Sensor is likely damaged.".format(T)
      e += "\nSetting the system to idle mode."
      print(e)
      thermostat.idle()
      notify_email(e)
      sys.exit()



def no_network():
    """
    If network connectivity lost, fallback_mode
    """
    pass


def notify_email(msg):
    """
    Email the passed message to address defined in config files.
    """

    # Import smtplib for the actual sending function
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    msg = MIMEText()
    msg['Subject'] = 'RPI Thermostat Warning'
    msg['From'] = email
    msg['To'] = email

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()


def notify_led():
    """
    blink LED indefinitely
    """

    print(rgb)
    led = RGBLED(2, 3, 4)
    while True:
        led.color(1,0,1)
        sleep(1)
        led.off()
        sleep(1)
        led.color(1,1,0)
        sleep(1)


if __name__ == "__main__":
    pass

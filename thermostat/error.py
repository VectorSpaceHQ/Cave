#!/usr/bin/env python3
# Error Handling
#
# In all cases of errors, notify the user by email
# Use LED sequence to display that something is wrong
# If temp sensor lost, turn off
# If temps ridiculous, turn off
# If network connectivity lost, fallback_mode
from gpiozero import RGBLED

def unknown_temp():
    """
    """
    pass

def bad_temp():
    """
    """
    pass

def no_network():
    """
    """
    pass

def notify_email():
    """
    """
    import smtplib

    with open("gmail.txt", 'rb') as fp:
        user = str(fp.readline().strip())
        password = str(fp.readline().strip())

    #Next, log in to the server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.sendmail("spontarelliam@gmail.com", "adam@vector-space.org", "testing smtplib")
    server.close()
    print ('successfully sent the mail')
    # except:
    #     print( "failed to send mail")


def notify_led():
    """
    blink LED indefinitely
    """
    #read values from the config file
    config = configparser.ConfigParser()
    config.read(dname+"/thermostat.conf")
    
    rgb = config.get('main','RGB_LED')
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
    notify_led()

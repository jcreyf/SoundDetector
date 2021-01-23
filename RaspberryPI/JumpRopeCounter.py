#!/usr/bin/env python3
#***************************************************************#
# Application to count the number of rope jumps.                #
# This is using the DAOKI Sound Sensor to try detect the sound  #
# of the rope hitting the ground and use that to increment a    #
# counter on screen.                                            #
#---------------------------------------------------------------#
# 2021-01-22  jcreyf  v0.1  Initial version                     #
#***************************************************************#

import RPi.GPIO as GPIO
import time

counter = 0
port_sounddetector = 17


#
# Callback method that will get called each time the SoundDetector port goes either
# high or low:
#
def callbackSoundDetector(port_sounddetector):
  counter += 1
  if GPIO.input(port_sounddetector):
    print(f'H:{counter:5}')
  else:
    print(f'H:{counter:5}')


# Setting up the GPIO pins:
GPIO.setmode(GPIO.BCM)
GPIO.setup(port_sounddetector, GPIO.IN)

# Set a filter for an event trigger on the SoundDetector port.
# We want to get an event on both the high and low values of the port, using
# a debounce period of 300ms:
GPIO.add_event_detect(port_sounddetector, GPIO.BOTH, bouncetime=300)
# Attach our callback method:
GPIO.add_event_callback(port_sounddetector, callbackSoundDetector)

# Now loop:
while True:
  time.sleep(1)

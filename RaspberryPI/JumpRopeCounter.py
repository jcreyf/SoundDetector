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
from tkinter import *

_counter = 0
_port_sounddetector = 17
_sounddetector_bouncetime = 200
_pause = False


def callbackSoundDetector(_port_sounddetector):
  """
  Callback method that will get called each time the SoundDetector triggers
  """
  global _counter, _pause
  if not _pause:
    _counter += 1
    print(f'{_counter:5}')
    lbl['text'] = f'{_counter:5}'


def btnReset_Click():
  """
  Function to reset the counter when the reset button is clicked
  """
  global _counter
  _counter = 0
  print(f'{_counter:5}')
  lbl['text'] = f'{_counter:5}'


def btnPause_Click():
  """
  Function to pause/resume the counter when the pause button is clicked
  """
  global _pause
  if _pause:
    _pause=False
    btnPause.text="Resume"
  else:
    _pause=True
    btnPause.text="Pause"


# Setting up the GPIO pin to which the SoundSensor is connected:
GPIO.setmode(GPIO.BCM)
GPIO.setup(_port_sounddetector, GPIO.IN)

# Set a filter for an event trigger on the SoundDetector port.
# We want to get an event on both the high and low values of the port, using
# a debounce period of 300ms:
GPIO.add_event_detect(_port_sounddetector, GPIO.BOTH, bouncetime=_sounddetector_bouncetime)
# Attach our callback method:
GPIO.add_event_callback(_port_sounddetector, callbackSoundDetector)

# Now loop (the non-GUI version):
#while True:
#  time.sleep(1)

# Create the window object:
window = Tk()
window.title("JumpRope Counter")
window.geometry('350x200')

# Create the counter label on the window:
lbl = Label(window, text=f'{_counter:5}', font=("Arial Bold", 50))
lbl.grid(column=0, row=0)
lbl.pack()

# Add a clear button to reset the counter:
btnClear = Button(window, text="Reset", command=btnReset_Click)
btnClear.pack()

# Add a clear button to reset the counter:
btnPause = Button(window, text="Pause", command=btnPause_Click)
btnPause.pack()


# Now loop until the cows come home:
window.mainloop()

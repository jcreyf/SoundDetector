#!/usr/bin/env python3
#**********************************************************************************#
# Application to count the number of rope jumps.                                   #
# This is using the DAOKI Sound Sensor to try detect the sound of the rope hitting #
# the ground and use that to increment a counter on screen.                        #
#----------------------------------------------------------------------------------#
# 2021-01-22  jcreyf  v0.1  Initial version                                        #
#**********************************************************************************#

import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter.ttk import Frame, Button, Style

class Counter(tk.Frame):
  def __init__(self):
    """
    Constructor
    """
    super().__init__()
    self._counter = 0
    self._pause = False
    self._lblCounterCounter_textSize = 380
    self.initGUI()
    self._port_sounddetector = 17
    self._sounddetector_bouncetime = 200
    self.initHardware()

  def initGUI(self):
    """
    Generate the GUI
    """
    self.master.title("JumpRope Counter")
    self.style=Style()
    self.style.theme_use("default")
    self.pack(side="top", fill=tk.BOTH, expand=True)
    # Configure the grid:
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure(2, weight=1)
    # Create the counter label on the window:
    self._lblCounter = tk.Label(self, text=f'{self._counter:5}', font=("Arial Bold", self._lblCounterCounter_textSize), borderwidth=1)
    self._lblCounter.grid(row=0, column=0, columnspan=3)
    # Add a clear button to reset the counter:
    btnClear = tk.Button(self, width=20, text="Reset", font=("Arial Bold", 24), bg='#FFA500', command=self.btnReset_Click)
    btnClear.grid(row=1, column=0)
    # Add a pause button to pause/resume counting when taking breaks:
    self._btnPause_text = tk.StringVar()
    btnPause = tk.Button(self, width=20, textvariable=self._btnPause_text, font=("Arial Bold", 24), bg='#FFA500', command=self.btnPause_Click)
    self._btnPause_text.set("Pause")
    btnPause.grid(row=1, column=1)
    # Add an exit button to stop the app:
    btnExit = tk.Button(self, width=20, text="Exit", font=("Arial Bold", 24), bg='#FFA500', command=self.btnExit_Click)
    btnExit.grid(row=1, column=2)

  def btnReset_Click(self):
    """
    Function to reset the counter when the reset button is clicked
    """
    self._counter = 0
    self._lblCounter['text'] = f'{self._counter:5}'

  def btnPause_Click(self):
    """
    Function to pause/resume the counter when the pause button is clicked
    """
    if self._pause:
      self._pause=False
      self._btnPause_text.set("Pause")
    else:
      self._pause=True
      self._btnPause_text.set("Resume")

  def btnExit_Click(self):
    """
    Stop the app
    """
    quit()

  def initHardware(self):
    """
    Setup the IO ports and hardware event handling
    """
    # Setting up the GPIO pin to which the SoundSensor is connected:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self._port_sounddetector, GPIO.IN)
    # Set a filter for an event trigger on the SoundDetector port.
    # We want to get an event on both the high and low values of the port, using a debounce period of a number of milliseconds:
    GPIO.add_event_detect(self._port_sounddetector, GPIO.BOTH, bouncetime=self._sounddetector_bouncetime)
    # Attach our callback method:
    GPIO.add_event_callback(self._port_sounddetector, self.incrementCounter)

  def incrementCounter(self, gpioPortNumber):
    """
    Increment the counter
    """
    if not self._pause:
      self._counter+=1
      self._lblCounter['text'] = f'{self._counter:5}'



def main():
  """
  Create the window object and instantiate the app
  """
  window = tk.Tk()
  window.geometry('1360x700+0+0')
  counter=Counter()
  window.mainloop()

if __name__=='__main__':
  main()

import RPi.GPIO as GPIO
import time

from outlet import Outlet
from timer_thread import TimerThread

class OutletManager():
    
    # buttons is a dictionary containing button id as key(e.g. on1) 
    # and pin number as the value
    def __init__(self, buttons, outlets):
        self.outlets = {}
        self.create_outlets(buttons) 

    def create_outlets(self, buttons):
        for outlet, pins in buttons:
            if outlet not in self.outlets():
                self.outlets[outlet] = Outlet(pins) 
    
    def turn_off_all(self):
        for outlet in self.outlets:
            outlet.reset_timer()

    def activate(self, outlet, interval):
        self.outlets[outlet].set_timer(interval)

    def adjust_timer(self, outlet, new_interval):
        self.outlets[outlet].reset_timer(new_interval)

    def cancel_outlet(self, outlet):
        self.adjust_timer(outlet, 0)




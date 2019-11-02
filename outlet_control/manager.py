from outlet import Outlet
from timer import TimingManager

import time
import sys


class Manager():
    
    '''
    
    Outlets is a list containing dictionaries with buttons and pins
    
    e.g. with 3 outlets:
    [   {'buttons' : { 'on' : 27, 'off' : 25 }, 'id' : 1}, 
        {'buttons' : { 'on' : 12, 'off' : 14 }, 'id' : 2}, 
        {'buttons' : { 'on' : 11, 'off' : 10 }, 'id' : 3} 
    ]
    
    '''

    def __init__(self, outlets):
        self.outlets = {}
        self.create_outlets(outlets)
    
    def create_outlets(self, outlets):
        for outlet in outlets:
            self.outlets[outlet['id']] = Outlet(outlet['buttons'])

    def is_active_outlet(self, outlet):
        print("Outlet in outlets:", outlet in self.outlets)
        print("Outlet is active:", self.outlets[outlet].is_active())
        return outlet in self.outlets and self.outlets[outlet].is_active()

    def activate_outlet(self, outlet, interval):
        if not self.is_active_outlet(outlet):
            self.outlets[outlet].activate(interval)
        else:
            self.outlets[outlet].adjust_time(interval)

    def deactivate_outlet(self, outlet):
        if self.is_active_outlet(outlet):
            self.outlets[outlet].deactivate()

    def deactivate_all_outlets(self):
        for outlet in self.outlets:
            self.deactivate_outlet(outlet)

from threading import Event,Lock
import RPi.GPIO as GPIO
import time

from button import Button
from timer_thread import TimerThread

class Outlet(Button):

    def __init__(self, pins):
        super().__init__(pins)
        self.event = Event()
        self.pins = pins
        self.lock = Lock()
        self.worker = None
   
    def is_active(self):
        return self.worker is not None
    '''
    Spawns a worker thread
    '''
    def activate(self, interval):
        if not self.is_active():
            self.worker = TimerThread(self, interval * 60)
            self.worker.start()

    def deactivate(self):
        if self.is_active():
            self.event.set()

    def adjust_time(self, interval):
        pass

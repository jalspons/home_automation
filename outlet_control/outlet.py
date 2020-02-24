import asyncio
import time

from queue import PriorityQueue
from threading import Event

from button import Button
from timerThread import TimerThread

class Outlet():

    def __init__(self, outlet_id, pins):
        self.id = outlet_id
        self.buttons = Button(pins)
        self.event = Event()
        self.worker = TimerThread(self, self.buttons)
        self.worker.start()
        self.requests = PriorityQueue()
        self.count = 0
   
    def new_request(self, task):
        start_time = task['activation_time']
        end_time = task['deactivation_time']
        print(f'Start: {start_time}, End: {end_time}')

        try:
            self.requests.put((start_time, end_time))
        except:
            return False

        return True

    def deactivate(self):
        self.worker.active = False
        self.worker.event.set()


    def ping_worker(self):
        # Ensure that own event is clear
        self.event.clear()

        # Set worker ping flag and event
        self.worker.ping = True
        self.worker.event.set()
        
        # Wait for 5 seconds to event turn
        tries = 3
        while not self.event.is_set() or tries > 0:
            self.event.wait(5)
            tries -= 1
        
        # If the trial count was exceeded and still not reply, 
        # deactive outlet if active and return False
        if tries < 1 and not self.event.is_set():
            if self.buttons.state:
                self.buttons.press_button('off')

            return False
        
        # Succesful pinging
        self.event.clear()
        return True

    def is_active(self):
        return self.worker.active

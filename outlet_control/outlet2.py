import asyncio
import time

from queue import PriorityQueue
from threading import Event

from button import Button
from timerThread import TimerThread

class Outlet():

    def __init__(self, pins):
        self.buttons = Button(pins)
        self.event = Event()
        self.worker = TimerThread(self, Button(pins), -1)
        self.worker.start()
        self.requests = PriorityQueue()
        self.count = 0
   
    def new_request(self, request):
        start_time = request['activation_time']
        end_time = request['deactivation_time']
        #print(f'Start: {start_time}, End: {end_time}')

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


    async def outlet_worker(self):
        self.outlet_event = Event()
        self.outlet_event.clear()

        self.worker_ping = False
        self.active_outlet = False
        self.task = None
        self.killtask = False
        self.waiting_period = 5 # Update the task for every 5 seconds

        while True:         
            # Wait until it is time to activate the outlet, or reset the task
            # variable to obtain new tasks.
            if self.task is not None:
                wait_time = min(self.task[0] - time.time(), self.waiting_period)
                if wait_time > 0:
                    self.event.wait(wait_time)
                    
            # If there are no outlets in the queue, wait until there are
            else:
                self.event.wait(self.waiting_period)

            # Activate outlet
            if self.time_to_start():
                # Change state and press button 'on'
                self.active = True 
                self.buttons.press_button('on')
                
                # Wait until the period has past or when event occurs
                self.event.wait(self.task[1] - time.time())
                # If worker is pinged while being active, reply and continue waiting
                while(self.ping and self.active):
                    self.reply_ping()
                    self.event.wait(self.task[1] - time.time())

                # Deactivate outlet, press button 'off' and reset task variable
                self.active = False
                self.buttons.press_button('off')             
                self.task = None
                
            # Respond to ping
            elif self.ping:
                #print(f'pinging time_to_start{self.time_to_start()}')
                self.reply_ping()
            
            # Put the current task back to the queue if it is unused
            if self.task is not None and self.task[0] > time.time():
                self.outlet.requests.put(self.task)

            # Obtain the next task with the lowest starting time from the queue
            if not self.outlet.requests.empty():  
                self.task = self.outlet.requests.get()
            
            # Clear the event flag
            self.event.clear()

    def time_to_start(self):
        t1 = time.time()
        #if self.task is not None:
            #print(f'time: {t1} {t1 > self.task[0]} {self.task[0] + (self.task[1] - self.task[0]) > t1}')
        
        return self.task is not None and \
                t1 > self.task[0] and \
                t1 < self.task[1]

    def reply_ping(self):
        self.ping = False
        self.outlet.event.set()

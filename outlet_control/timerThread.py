from threading import Event, Thread
import time

class TimerThread(Thread):
    def __init__(self, outlet, buttons):
        Thread.__init__(self)
        self.outlet = outlet
        self.event = Event()
        self.event.clear()
        self.activation = None
        self.ping = False
        self.active = False
        self.task = None
        self.waiting_period = 5 # Update the task for every 5 seconds

        # For error proofing, get pointers to buttons 
        self.buttons = outlet.buttons

    def run(self):
        while True:
            if self.task is not None:
                print(f'hello {self.outlet.id} {self.task[0] - time.time()}')            
            # Wait until it is time to activate the outlet, or reset the task
            # variable to obtain new tasks.
            if self.task is not None:
                wait_time = min(self.task[0] - time.time(), self.waiting_period)
                if wait_time > 0:
                    self.event.wait(wait_time)
                else:
                    if self.task[1] < time.time():
                        self.task = None
                    
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
        

        
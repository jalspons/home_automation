from threading import Event

from outlet import Outlet
from timer_thread import TimerThread

class TimingManager():
    
    def __init__(self, outlets):
        self.active_timers = {} # Dictionary containing Event objects linked with threads
        self.available_timers = len(outlets) # list containing all available outlets
        self.outlets = create_outlets(outlets)
        print(self.available_timers)
        self.threads = {}
        
    def create_outlets(self, outlets):
        for buttons in outlets: 
            self.outlets.append(Outlet(buttons)) 

    ### TIMING ###

    def set_timer(self, outlet, interval):
        if outlet in self.active_timers and len(self.available_timers) > outlet:
            return

        self.active_timers[outlet] = Event()
        self.threads[outlet] = TimerThread(self.outlets(outlet), 
                self.active_timers[outlet], interval * 60)
        self.threads[outlet].start()

    def is_active(self, outlet):
        return outlet in self.active_timers.keys()

    def is_active_thread(self, outlet):
        return self.is_active(outlet) or self.threads[outlet].is_alive()

    '''
    Each TimerThread has a lock activated on outlet objects.
    TimerThreads can be removed by sending an event to that specific thread
    '''
    def cancel_timer(self, outlet):
        if outlet in self.active_timers and len(self.available_timers) > outlet:
           self.active_timers[outlet].set()
           self.active_timers.pop(outlet)
           return True
        else:
           return False

    def reset_timer(self, outlet, new_interval = 0):
        if self.cancel_timer(outlet) and new_interval > 0:
            self.init_timer(outlet, new_interval)
            return True

        return False

    def cancel_all_timers(self):
        for outlet, event in self.active_timers:
            event.set()

        # TODO implement a way to check whether the threads are stopping


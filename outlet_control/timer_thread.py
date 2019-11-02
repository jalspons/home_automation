from threading import Thread

class TimerThread(Thread):
    def __init__(self, outlet, interval):
        Thread.__init__(self)
        self.outlet = outlet
        self.interval = interval

    def run(self):
        with self.outlet.lock:
            print("Pressing button _on_")
            #self.outlet.press_button('on')

            if not self.outlet.event.is_set():
                self.outlet.event.wait(self.interval*60)
            
            print("Pressing button _off_")
            #self.outlet.press_button('off')
            self.outlet.worker = None

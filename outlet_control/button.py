import RPi.GPIO as GPIO
import time

class Button():
    '''
    buttons is a dictionary containing the button and its GPIO pin
    e.g. {'on' : 21, 'off' : 22}
    '''
    def __init__(self, buttons):
        self.buttons = buttons
        self.setup_buttons()

    def setup_buttons(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        print(self.buttons['on'])
        for state in self.buttons:
            print('Setting for pin', self.buttons[state])# Not perhaps thread-safe and modify to use logging instead
            GPIO.setup(self.buttons[state], GPIO.OUT)

    def press_button(self, button):
        GPIO.output(self.buttons[button], GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(self.buttons[button], GPIO.LOW)
        time.sleep(0.2) 



import json
import time
import random
import unittest

from manager import Manager

# TODO event loop for listening server program

class TestingSuite(unittest.TestCase):
    
    def setUp(self):
        with open('outlets.json') as f:
            self.data = json.load(f)
        
        self.control = Manager(self.data)
        random.seed()

    # Test if worker active after adding a request
    def test_worker_not_active_after_adding_request_to_queue(self):
        self.control.new_outlet_request(1, {'activation_time': time.time() + 1, 'deactivation_time': time.time() + 5})
    
    # Test activating one request
    def test_activate_one_request(self):
        # Initially outlet should not be active
        self.assertFalse(self.control.is_active_outlet(1))
        # Add new request
        self.control.new_outlet_request(1, {'activation_time': time.time() + 0.5, 'deactivation_time': time.time() + 2})
        # Outlet should not be active
        self.assertFalse(self.control.is_active_outlet(1))
        # Outlet should not be active after request is put into the queue
        self.assertFalse(self.control.is_active_outlet(1))
        # Check worker is responsive
        self.assertTrue(self.control.ping_worker(1))
        # After 2 seconds the Outlet should be active
        time.sleep(1)
        # Now outlet should be active
        self.assertTrue(self.control.is_active_outlet(1))
        # Check worker responsive
        self.assertTrue(self.control.ping_worker(1))
        # Sleep over the active period
        time.sleep(2)
        # Outlet should not be active
        self.assertFalse(self.control.is_active_outlet(1))
        # Worker should be responsive
        self.assertTrue(self.control.ping_worker(1))

    def button_state_changes(self):
        button = self.control.outlets[1].buttons
        # Initially button's state should be false
        self.assertFalse(button.state)
        # Add new request
        self.control.new_outlet_request(1, {'activation_time': time.time() + 0.5, 'deactivation_time': time.time() + 2})
        # Button should not be active until it has been pressed
        self.assertFalse(button.state)
        time.sleep(1)
        # Button 'on' has been pressed and state should be true 
        self.assertTrue(button.state)
        # Sleep over the active period
        time.sleep(2)
        # Button 'off' has been pressed
        self.assertFalse(button.state)
        # There should be one 'on' button press
        self.assertEqual(button.count_on, 1)
        
    # Test with multiple requests
    def test_multiple_requests(self):
        # Transmit multiple requests
        button = self.control.outlets[1].buttons
        for i in range(1, 21):
            request = {'activation_time': time.time() + i , 'deactivation_time': time.time() + i + 0.5}
            self.control.new_outlet_request(1, request)

        time.sleep(30)
        # Check that all the requests have been registered
        self.assertEqual(button.count_on, 20)
        # Check that button off is pressed as the last button
        self.assertFalse(button.state)
        # Check that outlet is not active
        self.assertFalse(self.control.is_active_outlet(1))

        

    # Test with multiple requests with multiple random pings
    def test_multiple_requests_with_multiple_pings(self):
        # Transmit multiple requests
        button = self.control.outlets[1].buttons
        total_sleep = 0.0
        ping_count = 0

        for i in range(1, 21):
            request = {'activation_time': time.time() + i, 'deactivation_time': time.time() + i + 0.5}
            self.control.new_outlet_request(1, request)

        
        #await asyncio.sleep(5)
        for i in range(0, 50):
            r = random.random()
            if self.control.ping_worker(1):
                ping_count += 1

            time.sleep(r)
            total_sleep += r

        time.sleep(30 - total_sleep)

        # Check that all pings have occurred
        self.assertEqual(ping_count, 50)
         # Check that all the requests have been registered
        self.assertEqual(button.count_on, 20)
        # Check that button off is pressed as the last button
        self.assertFalse(button.state)
        # Check that outlet is not active
        self.assertFalse(self.control.is_active_outlet(1))


if __name__ == '__main__':
    unittest.main()
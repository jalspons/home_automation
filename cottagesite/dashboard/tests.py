from django.test import TestCase
from django.utils import timezone

from .models import Activation

class ActivationModelTests(TestCase):
# USER RELATED TESTS
    def owner_field_not_blank(self):
        pass

    def check_user_privileges(self):
        pass

# OUTLET RELATED TESTS
    def outlet_field_not_blank(self):
        pass

    def accept_only_existing_outlets(self):
        pass

# TIME-RELATED TESTS
    def no_duplicate_activations_for_a_time_period(self):
        pass

    def activation_time_is_now_or_future(self):
        pass

    def activation_time_is_earlier_than_deactivation_time(self):
        pass

    
# Create your tests here.

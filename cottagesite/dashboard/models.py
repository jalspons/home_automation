from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Outlet(models.Model):
    outlet_number = models.IntegerField(blank=False)
    description = models.CharField(default='Outlet object', max_length=200)

    def __str__(self):
        return str(self.outlet_number)
    
class Activation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    outlet = models.ManyToManyField(Outlet)
    activation_time = models.DateTimeField(blank=False)
    deactivation_time = models.DateTimeField(blank=False)

    def __str__(self):
        return str(self.activation_time)

    def is_active(self):
        return self.activation_time < timezone.now() and \
                self.deactivation_time > timezone.now()

    def is_in_future(self):
        return self.activation_time > timezone.now()

# Create your models here.

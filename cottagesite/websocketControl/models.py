from django.db import models

class Client(models.Model):
    client_types = [('CTRL', 'control')]
    channel_name = models.CharField(blank=False, max_length=100)
    channel_type = models.CharField(blank=False, max_length=100, 
                                    choices=client_types)

    def __str__(self):
        return str(self.channel_name)
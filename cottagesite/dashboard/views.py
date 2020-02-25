from asgiref.sync import async_to_sync

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.generic import ListView, FormView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils import timezone

from channels.layers import get_channel_layer
import json
import datetime

from .forms import ActivationForm
from .models import Activation, Outlet
from websocketControl.models import Client

@login_required
def activation_create_view(request):
    form = ActivationForm(request.POST or None) 
    if form.is_valid():
        activation = form.save(commit=False)
        activation.owner = request.user
        activation.save()
             
        data = form.cleaned_data
        channel_layer = get_channel_layer()
        
        outlet_data = {}
        for outlet in data['outlet']:
            activation.outlet.add(outlet)
            outlet_data[str(outlet)] = {
                'activation_time': data['activation_time'].timestamp(),
                'deactivation_time': data['deactivation_time'].timestamp()
            }
        
        message = {
            'type': 'chat.message',         # For django_redis
            'request': {
                'recipient': 'outlet_control',
                'sender': 'web-server',
                'request_type': 'ACTIVATION',
                'outlet_data': outlet_data
            }
        }

        async_to_sync(channel_layer.group_send)('CONTROLGROUP', message)

    context = { 'form': form }
    
    return render(request, 'dashboard/activation_create.html', context)
    

@login_required
def index(request):
    outlets = Outlet.objects.all()
    activations  = Activation.objects.filter(
        deactivation_time__gt=datetime.datetime.now()). \
            order_by('deactivation_time').order_by('activation_time')[:10]

    return render(request, 'dashboard/index.html', 
            {'outlets' : outlets, 'activations' : activations})

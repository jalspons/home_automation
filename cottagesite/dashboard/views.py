from asgiref.sync import async_to_sync

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

from .forms import ActivationForm
from .models import Activation, Outlet
from websocketControl.models import Client

@login_required
def activation_create_view(request):
    initial_data = {
        'owner': request.user.username
    }
    form = ActivationForm(request.POST or None, initial=initial_data) 
    if form.is_valid():
        data = form.cleaned_data
        channel_layer = get_channel_layer()

        response = {
            'type': 'chat.message',
            'request_type': 'ACTIVATION',
            'outlet': [str(outlet.outlet_number) for outlet in data['outlet']],
            #'activation_time': data['activation_time'],
            #'deactivation_time': data['deactivation_time']
        }

        async_to_sync(channel_layer.group_send)('CONTROLGROUP', response)

    context = { 'form': form }
    
    return render(request, 'dashboard/activation_create.html', context)
    

@login_required
def index(request):
    outlets = Outlet.objects.all()
    activations  = Activation.objects.all()
    active_or_upcoming_activations = [ activation.is_active() for activation in activations ]
    print(active_or_upcoming_activations)

    return render(request, 'dashboard/index.html', 
            {'outlets' : outlets, 
                'activations' : active_or_upcoming_activations})

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/index.html'
    model = Activation 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
           
        context['outlets'] = Outlet.objects.all()
        context['activations'] = Activation.objects.all()
        return context

class ActivationCreateView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/activation_create.html'
    form_class = ActivationForm
    success_url = '/'

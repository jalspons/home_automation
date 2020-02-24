from django import forms
from django.contrib.auth.models import User
from tempus_dominus.widgets import DateTimePicker

from .models import Activation, Outlet


class ActivationForm(forms.ModelForm):
    outlet = forms.ModelMultipleChoiceField(required=True,
            queryset=Outlet.objects.all(),
            widget=forms.CheckboxSelectMultiple())
    activation_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    deactivation_time = activation_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = Activation
        exclude = ['owner']
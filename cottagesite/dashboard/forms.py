from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime

from .models import Activation, Outlet

class ActivationForm(forms.ModelForm):
    owner = forms.CharField(max_length=50, widget=forms.HiddenInput())
    outlet = forms.ModelMultipleChoiceField(required=True,
            queryset=Outlet.objects.all(),
            widget=forms.CheckboxSelectMultiple(attrs={
                'class': 'btn-group btn-group-toggle'}))

    #activation_time = forms.DateTimeField(required=False, widget=AdminSplitDateTime())
    #deactivation_time = forms.DateTimeField(required=False, widget=AdminSplitDateTime())

    class Meta:
        model = Activation
        fields = [
                #'owner',
                'outlet'
                #'activation_time',
                #'deactivation_time'
        ]

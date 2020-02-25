from django import forms


from .models import Activation, Outlet


class ActivationForm(forms.ModelForm):
    outlet = forms.ModelMultipleChoiceField(
        queryset=Outlet.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
                'class': 'required form-check form-control'}))

    class Meta:
        model = Activation
        exclude = ['owner']

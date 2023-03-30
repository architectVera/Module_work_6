from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from order.models import Purchase


class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity', 'showdata']
        labels = {
            'quantity': 'quantity',
            'showdata': 'showdata',
        }

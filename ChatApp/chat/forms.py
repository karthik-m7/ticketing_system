from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    """Form for visitors to submit a ticket."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    number = forms.CharField(max_length=15)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

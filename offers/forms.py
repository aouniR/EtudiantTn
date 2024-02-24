from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'company', 'location', 'level', 'salary', 'offer_type', 'period', 'description']

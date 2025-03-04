
from django import forms
from .models import charity_table

class CharityForm(forms.ModelForm):
    class Meta:
        model = charity_table
        fields = ['title', 'place', 'type', 'description']

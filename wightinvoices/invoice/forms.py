from django import forms
from . import models


class Invoice(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ('name', 'client', 'comments')

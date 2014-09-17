from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from . import models


class Client(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ('name', 'address')

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'name',
            'address',
        )

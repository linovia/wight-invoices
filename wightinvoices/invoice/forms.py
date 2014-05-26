from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from . import models


class Invoice(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ('name', 'client', 'comments')

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            'name',
            'client',
            'comments',
        )

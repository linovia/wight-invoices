from django import forms
from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from . import models


class Invoice(forms.ModelForm):
    cc = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False)
    class Meta:
        model = models.Invoice
        fields = ('name', 'client', 'cc', 'notes')

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
            Field('cc', css_class="chosen-select"),
            'notes',
        )


class InvoiceItem(forms.ModelForm):
    class Meta:
        model = models.InvoiceItem
        fields = ('description', 'quantity', 'vat', 'amount')


class InvoiceItemHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InvoiceItemHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'form-inline'
        self.template = 'invoice/invoice_form_formset.html'


class InvoiceComment(forms.ModelForm):
    class Meta:
        model = models.InvoiceComment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super(InvoiceComment, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'comment',
            Submit('submit', 'Submit', css_class='button white'))


class Estimate(Invoice):
    class Meta(Invoice.Meta):
        model = models.Estimate


class EstimateItem(InvoiceItem):
    class Meta(InvoiceItem.Meta):
        model = models.EstimateItem

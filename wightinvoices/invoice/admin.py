from django.contrib import admin
from . import models


class ClientAdmin(admin.ModelAdmin):
    pass


class InvoiceItemInline(admin.TabularInline):
    model = models.InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceItemInline
    ]


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)

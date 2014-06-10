from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from . import models


class ClientAdmin(admin.ModelAdmin):
    pass


class InvoiceItemInline(admin.TabularInline):
    model = models.InvoiceItem


class InvoiceAdmin(GuardedModelAdmin):
    inlines = [
        InvoiceItemInline
    ]


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)

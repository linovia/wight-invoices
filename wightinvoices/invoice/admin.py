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


class EstimateItemInline(admin.TabularInline):
    model = models.EstimateItem


class EstimateAdmin(GuardedModelAdmin):
    inlines = [
        EstimateItemInline
    ]


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Estimate, EstimateAdmin)

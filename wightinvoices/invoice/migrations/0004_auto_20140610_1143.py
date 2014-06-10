# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


def fill_owner(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Invoice = apps.get_model("invoice", "Invoice")
    if len(Invoice.objects.all()) == 0:
        return
    User = apps.get_model("auth", "User")
    user = User.objects.all().order_by("id")[0]
    for invoice in Invoice.objects.all():
        invoice.owner = user
        invoice.save()


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_invoice_owner'),
    ]

    operations = [
        migrations.RunPython(fill_owner),
    ]

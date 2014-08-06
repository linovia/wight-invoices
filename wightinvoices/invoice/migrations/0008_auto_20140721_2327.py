# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_estimate_estimateitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'permissions': (('view_invoice', 'View invoice'),)},
        ),
        migrations.AlterField(
            model_name='estimate',
            name='status',
            field=models.CharField(default='draft', max_length=64, choices=[('draft', 'Draft'), ('sent', 'Sent'), ('accepted', 'Accepted'), ('refused', 'Refused')]),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(default='draft', max_length=64, choices=[('draft', 'Draft'), ('unpaid', 'Unpaid'), ('late', 'Late'), ('paid', 'Paid'), ('canceled', 'Canceled')]),
        ),
    ]

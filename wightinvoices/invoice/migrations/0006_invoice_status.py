# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20140610_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(max_length=64, default='unpaid', choices=[('draft', 'Draft'), ('unpaid', 'Unpaid'), ('canceled', 'Canceled'), ('paid', 'Paid')]),
            preserve_default=True,
        ),
    ]

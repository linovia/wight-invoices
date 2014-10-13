# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 10, 12, 59, 30, 382360), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 10, 12, 59, 47, 451776), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estimate',
            name='client',
            field=models.ForeignKey(to='clients.Client', related_name='estimates'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(to='clients.Client', related_name='invoices'),
        ),
    ]

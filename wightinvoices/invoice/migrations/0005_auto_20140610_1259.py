# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20140610_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id'),
        ),
    ]

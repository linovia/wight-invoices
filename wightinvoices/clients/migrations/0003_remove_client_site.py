# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20140916_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='site',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_estimatecomment_invoicecomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estimate',
            old_name='comments',
            new_name='notes',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='comments',
            new_name='notes',
        ),
    ]

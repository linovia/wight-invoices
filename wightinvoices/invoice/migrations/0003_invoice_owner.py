# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0002_auto_20140501_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]

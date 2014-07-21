# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action_time', models.DateTimeField(verbose_name='action time', auto_now=True)),
                ('object_id', models.TextField(blank=True, null=True, verbose_name='object id')),
                ('object_repr', models.CharField(verbose_name='object repr', max_length=200)),
                ('action', models.CharField(verbose_name='action flag', max_length=32)),
                ('content_type', models.ForeignKey(null=True, to='contenttypes.ContentType', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-action_time',),
                'verbose_name': 'history',
            },
            bases=(models.Model,),
        ),
    ]

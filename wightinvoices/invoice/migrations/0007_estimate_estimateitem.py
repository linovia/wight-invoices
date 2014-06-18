# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0006_invoice_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('comments', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=64, choices=[('draft', 'Draft'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='draft')),
                ('client', models.ForeignKey(to='invoice.Client', to_field='id')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
            ],
            options={
                'permissions': (('view_estimate', 'View estimate'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstimateItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256)),
                ('quantity', models.IntegerField()),
                ('vat', models.DecimalField(max_digits=4, decimal_places=2)),
                ('amount', models.DecimalField(max_digits=11, decimal_places=2)),
                ('estimate', models.ForeignKey(to='invoice.Estimate', to_field='id')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_remove_client_site'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('sent', 'Sent'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='draft', max_length=64)),
                ('client', models.ForeignKey(related_name='estimate', to='clients.Client')),
                ('owner', models.ForeignKey(related_name='owned_estimates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_estimate', 'View estimate'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstimateComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('estimate', models.ForeignKey(related_name='comments', to='invoice.Estimate')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstimateItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=256)),
                ('quantity', models.IntegerField()),
                ('vat', models.DecimalField(max_digits=4, decimal_places=2)),
                ('amount', models.DecimalField(max_digits=11, decimal_places=2)),
                ('estimate', models.ForeignKey(related_name='items', to='invoice.Estimate')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('unpaid', 'Unpaid'), ('late', 'Late'), ('paid', 'Paid'), ('canceled', 'Canceled')], default='draft', max_length=64)),
                ('client', models.ForeignKey(related_name='invoice', to='clients.Client')),
                ('owner', models.ForeignKey(related_name='owned_invoices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_invoice', 'View invoice'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('invoice', models.ForeignKey(related_name='comments', to='invoice.Invoice')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=256)),
                ('quantity', models.IntegerField()),
                ('vat', models.DecimalField(max_digits=4, decimal_places=2)),
                ('amount', models.DecimalField(max_digits=11, decimal_places=2)),
                ('invoice', models.ForeignKey(related_name='items', to='invoice.Invoice')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

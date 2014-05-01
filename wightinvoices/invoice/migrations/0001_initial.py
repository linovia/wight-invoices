# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('address', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('comments', models.TextField()),
                ('client', models.ForeignKey(to_field='id', to='invoice.Client')),
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
                ('vat', models.DecimalField(decimal_places=2, max_digits=4)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('invoice', models.ForeignKey(to_field='id', to='invoice.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

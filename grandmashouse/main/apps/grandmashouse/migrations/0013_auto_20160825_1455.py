# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandmashouse', '0012_ordercontent_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercontent',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandmashouse', '0011_auto_20160825_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercontent',
            name='quantity',
            field=models.FloatField(default=1),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 01:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hopper', '0006_auto_20161226_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]

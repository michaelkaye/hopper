# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 02:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hopper', '0002_auto_20161225_0027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='name',
            new_name='title',
        ),
    ]

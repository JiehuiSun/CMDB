# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 03:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_server_latest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='latest',
            new_name='latest_date',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='asset',
        ),
    ]
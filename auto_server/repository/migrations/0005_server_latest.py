# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_serverrecord_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='latest',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-11 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0007_auto_20171010_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverrecord',
            name='name',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
    ]

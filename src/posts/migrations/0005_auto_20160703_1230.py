# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-03 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_read_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='read_time',
            field=models.IntegerField(default=0),
        ),
    ]

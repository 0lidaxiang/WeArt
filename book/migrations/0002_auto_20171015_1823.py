# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='location',
            field=models.CharField(max_length=100, verbose_name=b'\xe5\xad\x98\xe5\x84\xb2\xe4\xbd\x8d\xe7\xbd\xae'),
        ),
    ]
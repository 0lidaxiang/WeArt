# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommand', '0004_auto_20171015_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommand',
            name='id',
            field=models.AutoField(max_length=20, primary_key=True, serialize=False, verbose_name=b'\xe7\xb7\xa8\xe8\x99\x9f'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 23:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommand', '0013_auto_20171015_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recommand',
            options={'verbose_name': '\u66f8\u7c4d\u63a8\u85a6', 'verbose_name_plural': '\u66f8\u7c4d\u63a8\u85a6\u5217\u8868\u7ba1\u7406'},
        ),
        migrations.AlterField(
            model_name='recommand',
            name='createTime',
            field=models.DateTimeField(auto_now_add=True, max_length=50, verbose_name=b'\xe7\x94\xb3\xe8\xab\x8b\xe6\x99\x82\xe9\x96\x93'),
        ),
        migrations.AlterField(
            model_name='recommand',
            name='id',
            field=models.AutoField(max_length=20, primary_key=True, serialize=False, verbose_name=b'\xe7\xb7\xa8\xe8\x99\x9f'),
        ),
        migrations.AlterField(
            model_name='recommand',
            name='modifyTime',
            field=models.DateTimeField(auto_now=True, max_length=50, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x99\x82\xe9\x96\x93'),
        ),
    ]

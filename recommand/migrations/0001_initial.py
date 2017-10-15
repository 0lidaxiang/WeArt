# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='recommand',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name=b'\xe7\xb7\xa8\xe8\x99\x9f')),
                ('idBook_id', models.CharField(max_length=100, unique=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb6\xe5\x90\x8d')),
                ('status', models.CharField(choices=[(b'allowed', b'allowed'), (b'abuse', b'abuse'), (b'locked', b'locked')], max_length=20, verbose_name=b'\xe7\x8b\x80\xe6\x85\x8b')),
                ('createTime', models.DateTimeField(max_length=50, verbose_name=b'\xe7\x94\xb3\xe8\xab\x8b\xe6\x99\x82\xe9\x96\x93')),
                ('modifyTime', models.DateTimeField(max_length=50, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x99\x82\xe9\x96\x93')),
            ],
            options={
                'db_table': 'recommand',
                'verbose_name': '\u63a8\u85a6\u8868',
                'verbose_name_plural': '\u63a8\u85a6\u5217\u8868\u7ba1\u7406',
            },
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-12 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headers',
            field=models.ImageField(default='static/images/headers/default.png', upload_to='static/uepload/static/headers/', verbose_name='用户头像'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-12 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20181012_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='article_num',
            field=models.IntegerField(default=0, verbose_name='发表文章的数量'),
        ),
    ]

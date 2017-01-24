# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_auto_20170123_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='score',
        ),
        migrations.AddField(
            model_name='link',
            name='rank_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='link',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Headline'),
        ),
    ]

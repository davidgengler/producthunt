# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 22:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_auto_20170123_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='author',
            new_name='submitter',
        ),
        migrations.RemoveField(
            model_name='link',
            name='thumbnail',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 20:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75, verbose_name='Headline')),
                ('thumbnail', models.URLField(blank=True, max_length=250, verbose_name='Thumbnail')),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
                ('url', models.URLField(blank=True, max_length=250, verbose_name='URL')),
                ('description', models.TextField(blank='True')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='links.Link')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

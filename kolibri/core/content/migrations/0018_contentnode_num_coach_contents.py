# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-16 15:19
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("content", "0017_auto_20190415_1855")]

    operations = [
        migrations.AddField(
            model_name="contentnode",
            name="num_coach_contents",
            field=models.IntegerField(blank=True, default=0, null=True),
        )
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-25 21:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rescuespot'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rescues',
        ),
    ]

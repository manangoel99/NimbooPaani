# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-26 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20181026_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourcesNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.TextField()),
                ('qty', models.IntegerField()),
                ('unit', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='resourcesavail',
            name='cid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.Camps'),
            preserve_default=False,
        ),
    ]

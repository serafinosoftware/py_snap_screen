# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-20 16:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osm_web', '0005_ask_stake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ask',
            name='price',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000000)]),
        ),
        migrations.AlterField(
            model_name='ask',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]

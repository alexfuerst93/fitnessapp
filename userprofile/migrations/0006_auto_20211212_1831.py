# Generated by Django 3.1.3 on 2021-12-12 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20211212_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise_pool',
            name='high_range',
            field=models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='exercise_pool',
            name='low_range',
            field=models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='exercise_pool',
            name='mid_range',
            field=models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]

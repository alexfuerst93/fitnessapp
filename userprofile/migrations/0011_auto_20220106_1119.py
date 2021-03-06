# Generated by Django 3.2.9 on 2022-01-06 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_auto_20211229_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise_pool',
            name='high_range',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='exercise_pool',
            name='low_range',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='exercise_pool',
            name='mid_range',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]

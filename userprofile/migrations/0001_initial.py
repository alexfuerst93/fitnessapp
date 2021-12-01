# Generated by Django 3.1.3 on 2021-11-06 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise_Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Name of Exercise')),
                ('max_calc', models.BooleanField(verbose_name='Include in Max-Calculator')),
            ],
        ),
    ]
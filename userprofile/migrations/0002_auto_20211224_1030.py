# Generated by Django 3.1.3 on 2021-12-24 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_set_I',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_set_II',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_set_III',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_set_IIII',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_set_IIIII',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_set_IIIIII',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_1_setcount',
            field=models.CharField(default='III', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_2_setcount',
            field=models.CharField(default='IIII', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_3_setcount',
            field=models.CharField(default='II', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_4_setcount',
            field=models.CharField(default='II', max_length=10),
            preserve_default=False,
        ),
    ]

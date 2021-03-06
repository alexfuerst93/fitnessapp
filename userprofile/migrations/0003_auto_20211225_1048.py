# Generated by Django 3.1.3 on 2021-12-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20211224_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workoutplan',
            old_name='exercise_1_set_I',
            new_name='exercise_1_set_1',
        ),
        migrations.RenameField(
            model_name='workoutplan',
            old_name='exercise_1_set_II',
            new_name='exercise_1_set_2',
        ),
        migrations.RenameField(
            model_name='workoutplan',
            old_name='exercise_1_set_III',
            new_name='exercise_1_set_3',
        ),
        migrations.RenameField(
            model_name='workoutplan',
            old_name='exercise_1_set_IIII',
            new_name='exercise_1_set_4',
        ),
        migrations.RenameField(
            model_name='workoutplan',
            old_name='exercise_1_set_IIIII',
            new_name='exercise_2_set_1',
        ),
        migrations.RenameField(
            model_name='workoutplan',
            old_name='exercise_1_set_IIIIII',
            new_name='exercise_2_set_2',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='exercise_1_setcount',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='exercise_2_setcount',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='exercise_3_setcount',
        ),
        migrations.RemoveField(
            model_name='workoutplan',
            name='exercise_4_setcount',
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='day_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_2_set_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_2_set_4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_3_set_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_3_set_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_3_set_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_3_set_4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_4_set_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_4_set_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_4_set_3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercise_4_set_4',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

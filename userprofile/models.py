from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.forms.fields import DecimalField

class MaxValue(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.CharField("Name of Exercise", max_length=100)
    max_value = models.DecimalField(max_digits=5, decimal_places=2)
    #SHOULD BE AN INTEGER
    timestamp = models.DateTimeField()
    # blank=True makes the field optional
    # null=True allows to write NULL to the database

    def __str__(self):
        return self.exercise

musclegroups = [
    ("legs", "Legs"),
    ("chest", "Chest"),
    ("back", "Back"),
    ("shoulders", "Shoulders"),
    ("biceps", "Biceps"),
    ("triceps", "Triceps"),
    ("core", "Core"),
    ("calves", "Calves")
    ]

class Exercise_Pool(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Name of Exercise", max_length=100)
    muscle = models.CharField("Musclegroup", max_length=50, choices=musclegroups, default="chest")
    high_range = models.DecimalField(blank=True, default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]) #weight
    mid_range = models.DecimalField(blank=True, default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]) #weight
    low_range = models.DecimalField(blank=True, default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]) #weight
    
    def __str__(self):
        return self.title


class WorkoutPlan(models.Model):
    # sole purpose of this model is to read from the other 2 tables and present results as one macrocycle
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle_name = models.CharField(max_length=50)
    week_count = models.IntegerField()
    day_count = models.IntegerField()
    day_completed = models.BooleanField(default=False)
    max_weight_percentage = models.IntegerField(default = 0)

    exercise_1 = models.CharField(blank=True, null=True, max_length=100)
    exercise_1_weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    exercise_1_set_1 = models.IntegerField(blank=True, null=True) # achieved reps per set
    exercise_1_set_2 = models.IntegerField(blank=True, null=True)
    exercise_1_set_3 = models.IntegerField(blank=True, null=True)
    exercise_1_set_4 = models.IntegerField(blank=True, null=True)

    exercise_2 = models.CharField(blank=True, null=True, max_length=100)
    exercise_2_weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    exercise_2_set_1 = models.IntegerField(blank=True, null=True)
    exercise_2_set_2 = models.IntegerField(blank=True, null=True)
    exercise_2_set_3 = models.IntegerField(blank=True, null=True)
    exercise_2_set_4 = models.IntegerField(blank=True, null=True)

    exercise_3 = models.CharField(blank=True, null=True, max_length=100)
    exercise_3_weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    exercise_3_set_1 = models.IntegerField(blank=True, null=True)
    exercise_3_set_2 = models.IntegerField(blank=True, null=True)
    exercise_3_set_3 = models.IntegerField(blank=True, null=True)
    exercise_3_set_4 = models.IntegerField(blank=True, null=True)

    exercise_4 = models.CharField(blank=True, null=True, max_length=100)
    exercise_4_weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    exercise_4_set_1 = models.IntegerField(blank=True, null=True)
    exercise_4_set_2 = models.IntegerField(blank=True, null=True)
    exercise_4_set_3 = models.IntegerField(blank=True, null=True)
    exercise_4_set_4 = models.IntegerField(blank=True, null=True)

    timestamp = models.DateField()

    def __str__(self):
        return f"{self.cycle_name} + week:{self.week_count} + day:{self.day_count}"


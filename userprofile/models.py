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
    muscle = models.CharField("Name of Musclegroup", max_length=50, choices=musclegroups, default="chest")
    high_range = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)]) #weight
    # high_range_reps = 
    # add reps for every range (4 sets)
    # add default = 0 for ranges and reps
    mid_range = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)]) #weight
    low_range = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)]) #weight
    
    def __str__(self):
        return self.title

class WorkoutPlan(models.Model):
    # sole purpose of this model is to read from the other 2 tables and structure results in mesocycles
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle_name = models.CharField(max_length=50)
    week_count = models.IntegerField()
    day_count = models.IntegerField()
    exercise_1 = models.CharField(max_length=100)
    exercise_1_weight = models.DecimalField(max_digits=5, decimal_places=2)
    exercise_2 = models.CharField(max_length=100)
    exercise_2_weight = models.DecimalField(max_digits=5, decimal_places=2)
    exercise_3 = models.CharField(max_length=100)
    exercise_3_weight = models.DecimalField(max_digits=5, decimal_places=2)
    exercise_4 = models.CharField(max_length=100)
    exercise_4_weight = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateField()
    # should the achieved reps from the user be saved in here? --> NO / should be read from the 2 original models

    def __str__(self):
        return self.cycle_name
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator

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
    timestamp = models.DateTimeField()
    high_range = models.PositiveIntegerField(blank=True, default=0, validators=[MaxValueValidator(20)]) # 12 reps
    mid_range = models.PositiveIntegerField(blank=True, default=0, validators=[MaxValueValidator(20)]) # 10 reps
    low_range = models.PositiveIntegerField(blank=True, default=0, validators=[MaxValueValidator(20)]) # 8 reps
    
    def __str__(self):
        return self.title

# Model Forms: https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
# dislaying forms in templates: https://docs.djangoproject.com/en/3.2/topics/forms/#working-with-form-templates
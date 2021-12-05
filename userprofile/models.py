from django.contrib.auth.models import User
from django.db import models

class MaxValue(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    exercise = models.CharField("Name of Exercise", max_length=100)
    max_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) #result of calculator
    timestamp = models.DateTimeField(auto_now_add=True) #should take the current date at creation, but take no updates
    # blank makes the field optional
    # null=True allows to write NULL to the database

    def __str__(self):
        return self.exercise

class Exercise_Pool(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Name of Exercise", max_length=100)
    muscle = models.CharField("Name of Musclegroup", max_length=50)
    high_range = models.DecimalField(max_digits=5, decimal_places=2) # 12 reps
    mid_range = models.DecimalField(max_digits=5, decimal_places=2) # 10 reps
    low_range = models.DecimalField(max_digits=5, decimal_places=2) # 8 reps
    
    def __str__(self):
        return self.title
        


# All about models: https://docs.djangoproject.com/en/3.2/topics/db/models/
#  all about databases: https://docs.djangoproject.com/en/3.2/topics/db/queries/
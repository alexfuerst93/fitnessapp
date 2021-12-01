from django.contrib.auth.models import User
from django.db import models

class Exercise_Pool(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Name of Exercise", max_length=100)
    muscle = models.CharField("Name of Musclegroup", max_length=50)
    track_perform = models.CharField(max_length=5)
    
    def __str__(self):
        return self.title

class MaxValue(models.Model):
    #user_id
    exercise = models.CharField("Name of Exercise", max_length=100)
    max_value = models.DecimalField(max_digits=5, decimal_places=2) #result of calculator
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #should take the current date at creation, but take no updates

# All about models: https://docs.djangoproject.com/en/3.2/topics/db/models/
#  all about databases: https://docs.djangoproject.com/en/3.2/topics/db/queries/
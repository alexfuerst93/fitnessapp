from django.db import models

class Exercise_Pool(models.Model):
    #user_id
    title = models.CharField("Name of Exercise", max_length=100)
    max_calc = models.BooleanField("Include in Max-Calculator", null=True, blank=True)
    track_perform = models.BooleanField("Track Performance", null=True, blank=True)
    # muscle group (for sorting purposes) --> Should be a dropdown!
    
    def __str__(self):
        return self.title

class MaxValue(models.Model):
    #user_id
    exercise = models.CharField("Name of Exercise", max_length=100)
    max_value = models.DecimalField(max_digits=5, decimal_places=2) #result of calculator
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #should take the current date at creation, but take no updates

# All about models: https://docs.djangoproject.com/en/3.2/topics/db/models/
#  all about databases: https://docs.djangoproject.com/en/3.2/topics/db/queries/
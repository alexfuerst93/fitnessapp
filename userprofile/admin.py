from django.contrib import admin
from .models import MaxValue, Exercise_Pool, WorkoutPlan

admin.site.register(Exercise_Pool)
admin.site.register(MaxValue)
admin.site.register(WorkoutPlan)
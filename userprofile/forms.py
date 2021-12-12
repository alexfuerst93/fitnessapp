from django import forms
from django.forms import ModelForm
from .models import MaxValue, Exercise_Pool

class Exercise_Pool_Form(ModelForm):
    class Meta:
        model = Exercise_Pool
        fields = ["title", "muscle", "high_range", "mid_range", "low_range"]



class CreateMaxValue(forms.Form):
    # maxvalue = MaxValue.objects.all()
    # maxvalue_list = [entry.exercise for entry in maxvalue]
    # dropdown_exercises = []
    # for exercise in maxvalue_list:
    #     dropdown_exercises.append((exercise, exercise))
    # dropdown_exercises.insert(0, ("choose", "Choose your Exercise"))

    choose_exercise = forms.ModelChoiceField(empty_label="select", label="Choose an existing exercise", queryset=MaxValue.objects.all(), required=False)
    create_exercise = forms.CharField(label="Add new Exercise", max_length=100, required=False) 
    reps = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1.0)
    weight = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1.0)

from django import forms
from django.forms import ModelForm
from .models import MaxValue, Exercise_Pool

class Exercise_Pool_Form(ModelForm):
    class Meta:
        model = Exercise_Pool
        fields = ["title", "muscle", "high_range", "mid_range", "low_range"]


maxvalue = MaxValue.objects.all()
maxvalue_list = [value.exercise for value in maxvalue]
dropdown_exercises = []
for index, name in enumerate(maxvalue_list, 1):
    dropdown_exercises.append((index, name))
dropdown_exercises.insert(0, (0, "Choose your Exercise"))

class CreateMaxValue(forms.Form):
    choose_exercise = forms.ChoiceField(label="Choose an existing exercise", choices = dropdown_exercises, required=False)
    create_exercise = forms.CharField(label="Add new Exercise", max_length=100, required=False)
    reps = forms.DecimalField(max_digits=5, decimal_places=2)
    weight = forms.DecimalField(max_digits=5, decimal_places=2)

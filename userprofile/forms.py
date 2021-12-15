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

class ConfigureWorkout(forms.Form):
    max_exercise = forms.ModelChoiceField(empty_label="select", label="Choose Max Exercise", queryset=MaxValue.objects.all()) 
    sec_exercise = forms.ModelChoiceField(empty_label="select", label="Choose Sec Exercise", queryset=MaxValue.objects.all())
    # check if ALL exercises are displayed or just the ones created by this specific user

    def clean(self):
        cleaned_data = super(ConfigureWorkout, self).clean()
        max_exercise = cleaned_data.get("max_exercise")
        sec_exercise = cleaned_data.get("sec_exercise"),

        if not max_exercise and not sec_exercise:
            raise forms.ValidationError('Please fill in both fields.')
        
        if max_exercise and not sec_exercise:
            return cleaned_data
        
        if not max_exercise and sec_exercise:
            return cleaned_data

        return cleaned_data

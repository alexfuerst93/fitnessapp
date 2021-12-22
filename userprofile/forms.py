from django import forms
from django.forms import ModelForm
from .models import MaxValue, Exercise_Pool
from django.core.exceptions import ValidationError

class Exercise_Pool_Form(ModelForm):
    class Meta:
        model = Exercise_Pool
        fields = ["title", "muscle", "high_range", "mid_range", "low_range"]

class CreateMaxValue(forms.Form):
    choose_exercise = forms.ModelChoiceField(empty_label="select", label="Choose an existing exercise", queryset=MaxValue.objects.all(), required=False)
    create_exercise = forms.CharField(label="Add new Exercise", max_length=100, required=False) 
    reps = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1.0)
    weight = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1.0)

class ConfigureWorkout(forms.Form):
    sets = [("II", "2 Sets"), ("III", "3 Sets"), ("IIII", "4 Sets"), ("IIIII", "5 Sets"), ("IIIIII", "6 Sets")]

    # check if ALL exercises are displayed or just the ones created by this specific user
    first_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    first_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    first_sets = forms.ChoiceField(label="How many sets?", choices=sets, initial="IIII")
    second_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    second_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    second_sets = forms.ChoiceField(label="How many sets?", choices=sets, initial="IIII")
    third_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    third_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    third_sets = forms.ChoiceField(label="How many sets?", choices=sets, initial="IIII")
    fourth_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    fourth_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    fourth_sets = forms.ChoiceField(label="How many sets?", choices=sets, initial="IIII")


    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_max_exercise = cleaned_data.get("first_max_exercise")
    #     first_sec_exercise = cleaned_data.get("first_sec_exercise")

    #     if first_max_exercise and first_sec_exercise:   
    #         raise forms.ValidationError("Enter either a Max Exercise or a Secondary Exercise.")

    #     else:
    #         return cleaned_data
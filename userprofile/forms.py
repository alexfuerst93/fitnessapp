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
    max_exercise = forms.ModelChoiceField(empty_label="select", label="Choose Max Exercise", queryset=MaxValue.objects.all(), required=False) 
    sec_exercise = forms.ModelChoiceField(empty_label="select", label="Choose Sec Exercise", queryset=Exercise_Pool.objects.all(), required=False)
    # check if ALL exercises are displayed or just the ones created by this specific user

    def clean(self):
        cleaned_data = super().clean()
        max_exercise = cleaned_data.get("max_exercise")
        sec_exercise = cleaned_data.get("sec_exercise")

        if max_exercise and sec_exercise:
            raise forms.ValidationError("Enter either a Max Exercise or a Secondary Exercise.")

        else:
            return cleaned_data

# doc: https://docs.djangoproject.com/en/3.2/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
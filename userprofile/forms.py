from django import forms

class CreateExercise(forms.Form):
    name_of_exercise = forms.CharField(label="Add Exercise", max_length=100)
    #max_calc = forms.DecimalField(label="Enter your Max Value")
    #track_perform = forms.BooleanField(label="Track Performance", required=False)
    # timestamp is missing

# General information on forms: https://docs.djangoproject.com/en/3.2/topics/forms/
# Specific field information: https://docs.djangoproject.com/en/3.2/ref/forms/fields/
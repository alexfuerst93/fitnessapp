from django import forms

class CreateExercise(forms.Form):
    name_of_exercise = forms.CharField(label="Add Exercise", max_length=100)
    muscle = forms.ChoiceField(label="Primary Muscle", choices = [
        ("legs", "Legs"),
        ("chest", "Chest"),
        ("back", "Back"),
        ("shoulders", "Shoulders"),
        ("biceps", "Biceps"),
        ("triceps", "Triceps"),
        ("core", "Core"),
        ("calves", "Calves")
        ])
    track = forms.BooleanField(label="Track Performance", required=False)
    #max_value = forms.DecimalField(label="Enter your Max Value", required=False)
    #timestamp = forms.DateTimeField(auto_now=False, auto_now_add=True) #should take the current date at creation, but take no updates

# General information on forms: https://docs.djangoproject.com/en/3.2/topics/forms/
# Specific field information: https://docs.djangoproject.com/en/3.2/ref/forms/fields/
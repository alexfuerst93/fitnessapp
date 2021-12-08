from django import forms
from .models import MaxValue

musclegroups = [
        ("legs", "Legs"),
        ("chest", "Chest"),
        ("back", "Back"),
        ("shoulders", "Shoulders"),
        ("biceps", "Biceps"),
        ("triceps", "Triceps"),
        ("core", "Core"),
        ("calves", "Calves")
        ]

class CreateExercise(forms.Form):
    name_of_exercise = forms.CharField(label="Add Exercise", max_length=100)
    muscle = forms.ChoiceField(label="Primary Muscle", choices = musclegroups)
    track = forms.BooleanField(label="Track Performance", required=False)
    #max_value = forms.DecimalField(label="Enter your Max Value", required=False)
    #timestamp = forms.DateTimeField(auto_now=False, auto_now_add=True) #should take the current date at creation, but take no updates

maxvalue = MaxValue.objects.all()
maxvalue_list = []
for value in maxvalue:
    maxvalue_list.append(value.exercise)
dropdown_exercises = []
for index, name in enumerate(maxvalue_list, 1):
    dropdown_exercises.append((index, name))
    # return list of sets with "1, exercise"
dropdown_exercises.insert(0, (0, "Choose your Exercise"))
print(dropdown_exercises)

class CreateMaxValue(forms.Form):
    choose_exercise = forms.ChoiceField(label="Choose an existing exercise", choices = dropdown_exercises, required=False)
    create_exercise = forms.CharField(label="Add new Exercise", max_length=100, required=False)
    reps = forms.DecimalField(max_digits=5, decimal_places=2)
    weight = forms.DecimalField(max_digits=5, decimal_places=2)

    # def clean(self):
    #     cleaned_data = super(CreateMaxValue, self).clean()
    #     choose_exercise = cleaned_data.get("choose_exercise")
    #     create_exercise = cleaned_data.get("create_exercise")
    #     if choose_exercise == "0" and create_exercise == "":
    #         raise forms.ValidationError("Decide: Add a new max Value to a new or existing exercise.")
    #     elif choose_exercise != "0" and create_exercise != "":
    #         raise forms.ValidationError("You need to select an exercise or create a new one.")

    #     return cleaned_data


# General information on forms: https://docs.djangoproject.com/en/3.2/topics/forms/
# Specific field information: https://docs.djangoproject.com/en/3.2/ref/forms/fields/
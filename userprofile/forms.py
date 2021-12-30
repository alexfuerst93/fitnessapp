from django import forms
from django.forms import ModelForm
from .models import MaxValue, Exercise_Pool, WorkoutPlan
from django.core.exceptions import ValidationError

class Exercise_Pool_Form(ModelForm):
    class Meta:
        model = Exercise_Pool
        fields = ["title", "muscle", "high_range", "mid_range", "low_range"]

class CreateMaxValue(forms.Form):

    # overwrite __init__ to filter ModelChoiceField by user_id
    def __init__(self, request, *args, **kwargs):
        super(CreateMaxValue, self).__init__(*args, **kwargs)
        self.fields['choose_exercise'] = forms.ModelChoiceField(empty_label="select", label="Choose existing exercise", queryset=MaxValue.objects.filter(user_id=request), required=False)

    # choose_exercise = forms.ModelChoiceField(empty_label="select", label="Choose existing exercise", queryset=MaxValue.objects.all(), required=False)
    create_exercise = forms.CharField(label="Add new Exercise", max_length=100, required=False) 
    reps = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1.0)
    weight = forms.DecimalField(max_digits=5, decimal_places=2, min_value=1.0)

class ConfigureWorkout(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(ConfigureWorkout, self).__init__(*args, **kwargs)
        self.fields['first_max_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.filter(user_id=request), required=False)
        self.fields['first_sec_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.filter(user_id=request), required=False)
        self.fields['second_max_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.filter(user_id=request), required=False)
        self.fields['second_sec_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.filter(user_id=request), required=False)
        self.fields['third_max_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.filter(user_id=request), required=False)
        self.fields['third_sec_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.filter(user_id=request), required=False)
        self.fields['fourth_max_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.filter(user_id=request), required=False)
        self.fields['fourth_sec_exercise'] = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.filter(user_id=request), required=False)



    # first_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    # first_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    # second_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    # second_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    # third_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    # third_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)
    # fourth_max_exercise = forms.ModelChoiceField(empty_label="select", queryset=MaxValue.objects.all(), required=False) 
    # fourth_sec_exercise = forms.ModelChoiceField(empty_label="select", queryset=Exercise_Pool.objects.all(), required=False)

class AchievedReps(ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["exercise_1_set_1", "exercise_1_set_2", "exercise_1_set_3", "exercise_1_set_4",
        "exercise_2_set_1", "exercise_2_set_2", "exercise_2_set_3", "exercise_2_set_4",
        "exercise_3_set_1", "exercise_3_set_2", "exercise_3_set_3", "exercise_3_set_4",
        "exercise_4_set_1", "exercise_4_set_2", "exercise_4_set_3", "exercise_4_set_4"]
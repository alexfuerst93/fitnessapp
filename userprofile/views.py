from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.utils import timezone

#user creation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# database tables
from .models import MaxValue, Exercise_Pool, musclegroups, WorkoutPlan
from .forms import CreateMaxValue, Exercise_Pool_Form, ConfigureWorkout
from .helpers import epley

def startpage(request):
    if request.method == "GET":
        return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("profile") # render creates content and issues status code 200 / redirect issues a 302 to the browser
            except IntegrityError:
                return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm(), "error" : "User already exists"})
        else:
            return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm(), "error" : "Passwords do not match"})
                # all about users: https://docs.djangoproject.com/en/3.2/topics/auth/default/

def profile(request):
    #databases
    max_vals = MaxValue.objects.filter(user_id=request.user)
    exercises = Exercise_Pool.objects.filter(user_id=request.user)
    workout = WorkoutPlan.objects.filter(user_id=request.user)
    #form
    add_exercise = Exercise_Pool_Form()
    form_maxval = CreateMaxValue()
    
    sorted_musclegroups = [musclegroup[0] for musclegroup in musclegroups]
    sorted_musclegroups.sort()

    # retrieve unique values of all current cycles
    ### timestamp is missing ###
    cycles = list(set([cycle.cycle_name for cycle in workout]))

    render_dict = {
        "maxvals" : max_vals, "exercises" : exercises,
        "form_maxval" : form_maxval, "form" : add_exercise, 
        "musclegroups" : sorted_musclegroups,
        "cycles" : cycles
        }

    if request.method == "GET":
        return render(request, "userprofile/profile.html", render_dict)

    elif "calculated_maxrep" in request.POST:
        # form validations are missing
        result = epley(float(request.POST["weight"]), float(request.POST["reps"]))
        render_dict["ergebnis"] = f"Your Max value: {result}"
        return render(request, "userprofile/profile.html", render_dict)

    elif "calculate_and_safe" in request.POST:
        print(request.POST)
        # if form_maxval.is_valid(): # why isnt the form validating?
        if request.POST["choose_exercise"] == "" and request.POST["create_exercise"] == "":
            render_dict["error"] = "Select an exercise first."
            return render(request, "userprofile/profile.html", render_dict)
        elif request.POST["choose_exercise"] != "" and request.POST["create_exercise"] != "":
            render_dict["error"] = "Either choose an existing exercise or create a new one."
            return render(request, "userprofile/profile.html", render_dict)
        elif request.POST["create_exercise"] in [entry.exercise for entry in max_vals]:
            render_dict["error"] = "Exercise already exists."
            return render(request, "userprofile/profile.html", render_dict)

        elif request.POST["choose_exercise"] == "":
            result = epley(float(request.POST["weight"]), float(request.POST["reps"]))
            max_vals.create(user_id=request.user, exercise=request.POST["create_exercise"], max_value=result, timestamp=timezone.now())
            return redirect("profile")

        else:
            result = epley(float(request.POST["weight"]), float(request.POST["reps"]))
            update_max_value = MaxValue.objects.get(id = request.POST["choose_exercise"])
            update_max_value.max_value = result
            update_max_value.timestamp = timezone.now()
            update_max_value.save()
            return redirect("profile")

    elif "delete_maxval" in request.POST:
        print(request.POST)
        pk = [key for key in request.POST.keys()]
        deleted = MaxValue.objects.get(id = pk[1]).delete()
        return redirect("profile")

    elif "added_exercise" in request.POST:
        print(request.POST)
        if request.POST["title"] in [exercise.title for exercise in exercises]:
            render_dict["form_error"] = f"You already have an exercise called {request.POST['title']}!"
            return render(request, "userprofile/profile.html", render_dict)
        try:
            form_add_exercise = Exercise_Pool_Form(request.POST)
            new_exercise = form_add_exercise.save(commit=False)
            new_exercise.user_id = request.user
            new_exercise.save()
            return redirect("profile")
        except ValueError:
            render_dict["form_error"] = "You entered invalid data."
            return render(request, "userprofile/profile.html", render_dict)

    elif "deleted_exercise" in request.POST:
        print(request.POST)
        pk = [key for key in request.POST.keys()]
        Exercise_Pool.objects.get(id = pk[1]).delete()
        return redirect("profile")

    elif "modified_exercise" in request.POST:
        print(request.POST)
        pk = [key for key in request.POST.keys()]
        form_modify_exercise = Exercise_Pool.objects.get(id = pk[3]) # retrieve ID from model
        modified_exercise = Exercise_Pool_Form(request.POST, instance=form_modify_exercise) # create instance of that entry and plug it into the form
        modified_exercise.save() # update the model form based on POST data
        return redirect("profile")


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm()})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'userprofile/loginuser.html', {'form' : AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'userprofile/loginuser.html', {'form' : AuthenticationForm(), 'error' : "User not found / Or password did not match"})
        else:
            login(request, user)
            return redirect('profile')

def configure(request):

    if request.method == "GET":
        return render(request, "userprofile/configure.html")
    
    elif "day_amount" in request.POST:
        configure_workout_day1 = ConfigureWorkout()
        configure_workout_day2 = ConfigureWorkout()
        configure_workout_day3 = ConfigureWorkout()
        days = int(request.POST["days"])

        return render(request, "userprofile/configure.html", {
            "days" : days, 
            "configure_workout_day1" : configure_workout_day1,
            "configure_workout_day2" : configure_workout_day2,
            "configure_workout_day3" : configure_workout_day3
        })      

    elif "configuration_completed" in request.POST:
        days = int(request.POST["days"])
        # print(request.POST)
        # retrieve all the selected exercises from the post data. values are stored in a list, each index = 1 day
        first_max_exercise = request.POST.getlist("first_max_exercise")
        first_sec_exercise = request.POST.getlist("first_sec_exercise")
        second_max_exercise = request.POST.getlist("second_max_exercise")
        second_sec_exercise = request.POST.getlist("second_sec_exercise")
        third_max_exercise = request.POST.getlist("third_max_exercise")
        third_sec_exercise = request.POST.getlist("third_sec_exercise")
        fourth_max_exercise = request.POST.getlist("fourth_max_exercise")
        fourth_sec_exercise = request.POST.getlist("fourth_sec_exercise")

        # make form validations to ensure the user decided everytime between max and sec exercise
        if first_max_exercise[0] and first_sec_exercise[0]:
            error = "Select either a max exercise or a secondary exercise per day per row."
            configure_workout_day1 = ConfigureWorkout()
            configure_workout_day2 = ConfigureWorkout()
            configure_workout_day3 = ConfigureWorkout()
            return render(request, "userprofile/configure.html", {
                "error" : error,
                "days" : days, 
                "configure_workout_day1" : configure_workout_day1,
                "configure_workout_day2" : configure_workout_day2,
                "configure_workout_day3" : configure_workout_day3
            })

        # all configurations passed! Now build up the complete workout and send the user to it.
        else:
            #exercises = Exercise_Pool.objects.filter(user_id=request.user)
            #max_vals = MaxValue.objects.filter(user_id=request.user)
            cycle_name = "cycle2" #check if for pre-existing cycles and increment
            timestamp = timezone.now()

            exercise_1 = MaxValue.objects.get(pk = first_max_exercise[0])
            workout = WorkoutPlan(
                user_id = request.user,
                cycle_name = cycle_name, #needs a check of all previous cycles
                week = 1, # needs a for loop through all 16 weeks
                day = 1, # needs a for loop through all possible days (48/64/80)
                exercise_1 = exercise_1.exercise, #needs a conditional to check either max or sec exercise
                exercise_1_weight = float(exercise_1.max_value)*0.70,
                timestamp = timestamp
                )
            workout.save()

            return redirect("profile")
            # learn the database: https://docs.djangoproject.com/en/4.0/topics/db/queries/#creating-objects
            # stackoverflow: https://stackoverflow.com/questions/26672077/django-model-vs-model-objects-create

def workout(request, cycle):
    workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
    return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle})

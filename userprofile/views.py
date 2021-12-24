from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.utils import timezone
from datetime import date

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
        print(request.POST)

        # retrieve all the selected exercises and sets from the post data. values are stored in a list, each index = 1 day
        first_max_exercise = request.POST.getlist("first_max_exercise")
        first_sec_exercise = request.POST.getlist("first_sec_exercise")
        first_sets = request.POST.getlist("first_sets")
        second_max_exercise = request.POST.getlist("second_max_exercise")
        second_sec_exercise = request.POST.getlist("second_sec_exercise")
        second_sets = request.POST.getlist("second_sets")
        third_max_exercise = request.POST.getlist("third_max_exercise")
        third_sec_exercise = request.POST.getlist("third_sec_exercise")
        third_sets = request.POST.getlist("third_sets")
        fourth_max_exercise = request.POST.getlist("fourth_max_exercise")
        fourth_sec_exercise = request.POST.getlist("fourth_sec_exercise")
        fourth_sets = request.POST.getlist("fourth_sets")

        # make form validations to ensure the user decided everytime between max and sec exercise
        # selected sets are never none
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

        # all configurations passed! Now build up the complete workout.
        else:

            """ Global variables for a mesocycle """
            # get all currently existing cycles and increment the highest/latest by 1 to start a new cycle
            previous_cycles = WorkoutPlan.objects.filter(user_id=request.user)
            if previous_cycles:
                retrieve_unique_cycles = list(set([int(cycle.cycle_name[5:]) for cycle in previous_cycles]))
                cycle_name = "cycle" + str(max(retrieve_unique_cycles) + 1)
            else:
                cycle_name = "cycle1"

            timestamp = date.today()
            day_count = 1
            week_count = 1
            """ ------------------------------- """

            def selected_exercises(max, sec):
                # Determine whether the user selected a max exercise or a secondary exercise per row per day
                # Using the primary key from POST, search for the selected exercise in the corresponding table/model
                if max:
                    exercise = MaxValue.objects.get(pk = max)
                    return {"exercise" : exercise.exercise, "exercise_weight" : float(exercise.max_value)*0.70}
                elif sec:
                    exercise = Exercise_Pool.objects.get(pk = sec)
                    return {"exercise" : exercise.title, "exercise_weight" : exercise.high_range}
                else:
                    return {"exercise" : "", "exercise_weight" : 0.00}
                
            # loop over 1 week in the entire macrocycle
            for day in range(days):
                # Currently, POST data is stored in a list. Each index = 1 day
                exercise_1 = selected_exercises(first_max_exercise[day], second_max_exercise[day])
                exercise_2 = selected_exercises(second_max_exercise[day], second_sec_exercise[day])
                exercise_3 = selected_exercises(third_max_exercise[day], third_sec_exercise[day])
                exercise_4 = selected_exercises(fourth_max_exercise[day], fourth_sec_exercise[day])

                workout = WorkoutPlan(
                    user_id = request.user,
                    cycle_name = cycle_name,
                    week_count = week_count,
                    day_count = day_count,
                    exercise_1 = exercise_1["exercise"],
                    exercise_1_weight = exercise_1["exercise_weight"],
                    exercise_1_setcount = first_sets[day],
                    exercise_2 = exercise_2["exercise"], 
                    exercise_2_weight = exercise_2["exercise_weight"],
                    exercise_2_setcount = second_sets[day],
                    exercise_3 = exercise_3["exercise"], 
                    exercise_3_weight = exercise_3["exercise_weight"],
                    exercise_3_setcount = third_sets[day],
                    exercise_4 = exercise_4["exercise"], 
                    exercise_4_weight = exercise_4["exercise_weight"],
                    exercise_4_setcount = fourth_sets[day],
                    timestamp = timestamp
                    )
                workout.save()
                day_count += 1

            # better: direct the user to his newly created workout!
            # return workout(request, cycle_name)
            return redirect("profile")

def workout(request, cycle):
    workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
    
    if request.method == "GET":
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle})

    elif "workout_done" in request.POST:
        print(request.POST)
        todays_workout = get_object_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user, day_count=request.POST["day"])

        set_1 = request.POST.getlist("exercise_1")
        todays_workout.exercise_1_set_I = set_1[0]
        ### ??? dynamic length ??? ###

        # set boolean for achieved day
        # update WorkoutPlan with newly achieved reps
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle})


def contact(request):
    return render(request, "userprofile/contact.html")


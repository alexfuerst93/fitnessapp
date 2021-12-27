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
from .helpers import epley, check_input, workout_validator, workout_configurator

def startpage(request):
    if request.method == "GET":
        return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm()})
    else:
        # case 1: passwords do not match
        # case 2: user already exists
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("profile")
            except IntegrityError:
                return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm(), "error" : "User already exists!"})
        else:
            return render(request, "userprofile/startpage.html", {"create_user" : UserCreationForm(), "error" : "Passwords do not match!"})

def profile(request):
    #databases
    max_vals = MaxValue.objects.filter(user_id=request.user)
    exercises = Exercise_Pool.objects.filter(user_id=request.user)
    workout = WorkoutPlan.objects.filter(user_id=request.user)
    #forms
    add_exercise = Exercise_Pool_Form()
    form_maxval = CreateMaxValue()
    
    sorted_musclegroups = [musclegroup[0] for musclegroup in musclegroups]
    sorted_musclegroups.sort()

    # retrieve unique values of all current cycles
    all_cycles = list(set([cycle.cycle_name for cycle in workout]))
    current_cycle = max(all_cycles)

    # filters model to only contain unique cycle+timestamp combinations
    cycles = WorkoutPlan.objects.filter(user_id=request.user).values("cycle_name", "timestamp").order_by("-cycle_name").distinct()

    render_dict = {
        "maxvals" : max_vals, "exercises" : exercises,
        "form_maxval" : form_maxval, "form" : add_exercise, 
        "musclegroups" : sorted_musclegroups,
        "cycles" : cycles,
        "current_cycle" : current_cycle
        }

    if request.method == "GET":
        return render(request, "userprofile/profile.html", render_dict)

    elif "calculated_maxrep" in request.POST:
        # form validations are missing
        result = epley(float(request.POST["weight"]), float(request.POST["reps"]))
        render_dict["ergebnis"] = f"Your Max value: {result}"
        return render(request, "userprofile/profile.html", render_dict)

    elif "calculate_and_safe" in request.POST:
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
            return render(request, 'userprofile/loginuser.html', {'form' : AuthenticationForm(), 'error' : "User not found or password did not match!"})
        else:
            login(request, user)
            return redirect('profile')


def workout(request, cycle):
    if request.method == "GET":
        workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle})

    elif "workout_done" in request.POST:
        print(request.POST)

        # reminder: 1 entry in WorkoutPlan table = 1 day of training
        todays_workout = get_object_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user, day_count=request.POST["day"])

        # retrieve all achieved reps per sets per exercise from POST and update table
        ### use a modelform instead? ###
        if "exercise_1" in request.POST:
            sets_exercise_1 = request.POST.getlist("exercise_1")
            todays_workout.exercise_1_set_1 = sets_exercise_1[0]
            todays_workout.exercise_1_set_2 = sets_exercise_1[1]
            todays_workout.exercise_1_set_3 = sets_exercise_1[2]
            todays_workout.exercise_1_set_4 = sets_exercise_1[3]
        
        if "exercise_2" in request.POST:
            sets_exercise_2 = request.POST.getlist("exercise_2")
            todays_workout.exercise_2_set_1 = sets_exercise_2[0]
            todays_workout.exercise_2_set_2 = sets_exercise_2[1]
            todays_workout.exercise_2_set_3 = sets_exercise_2[2]
            todays_workout.exercise_2_set_4 = sets_exercise_2[3]

        if "exercise_3" in request.POST:
            sets_exercise_3 = request.POST.getlist("exercise_1")
            todays_workout.exercise_3_set_1 = sets_exercise_3[0]
            todays_workout.exercise_3_set_2 = sets_exercise_3[1]
            todays_workout.exercise_3_set_3 = sets_exercise_3[2]
            todays_workout.exercise_3_set_4 = sets_exercise_3[3]

        if "exercise_4" in request.POST:
            sets_exercise_4 = request.POST.getlist("exercise_1")
            todays_workout.exercise_4_set_1 = sets_exercise_4[0]
            todays_workout.exercise_4_set_2 = sets_exercise_4[1]
            todays_workout.exercise_4_set_3 = sets_exercise_4[2]
            todays_workout.exercise_4_set_4 = sets_exercise_4[3]

        todays_workout.day_completed = True
        todays_workout.save()

        workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle})
    
    else:
        workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle})



def configure(request):
    if request.method == "GET":
        return render(request, "userprofile/configure.html")

    elif "exercises_confirmed" in request.POST:
        return render(request, "userprofile/configure.html", {"step_1" : True})
    
    elif "day_amount" in request.POST:
        days = int(request.POST["days"])
        return render(request, "userprofile/configure.html", workout_configurator(days))

    elif "configuration_completed" in request.POST:
        days = int(request.POST["days"])
        print(request.POST)

        # retrieve all the selected exercises from the post data. values are stored in a list, each index = 1 day
        first_max_exercise = request.POST.getlist("first_max_exercise")
        print(first_max_exercise)

        first_sec_exercise = request.POST.getlist("first_sec_exercise")
        second_max_exercise = request.POST.getlist("second_max_exercise")
        second_sec_exercise = request.POST.getlist("second_sec_exercise")
        third_max_exercise = request.POST.getlist("third_max_exercise")
        third_sec_exercise = request.POST.getlist("third_sec_exercise")
        fourth_max_exercise = request.POST.getlist("fourth_max_exercise")
        fourth_sec_exercise = request.POST.getlist("fourth_sec_exercise")

        # now validate the user's input
        if not check_input([first_max_exercise, first_sec_exercise, second_max_exercise, second_sec_exercise, third_max_exercise, third_sec_exercise, fourth_max_exercise, fourth_sec_exercise]):
            # all lists are empty, which means the user didn't select a single exercise
            setup = workout_configurator(days)
            setup["error"] = "You didnt' select an exercise."
            return render(request, "userprofile/configure.html", setup)

        elif not all([workout_validator(days, first_max_exercise, first_sec_exercise), workout_validator(days, second_max_exercise, second_sec_exercise), 
                    workout_validator(days, third_max_exercise, third_sec_exercise), workout_validator(days, fourth_max_exercise, fourth_sec_exercise)]):
            # make form validations to ensure the user decided everytime between max and sec exercise
            setup = workout_configurator(days)
            setup["error"] = "Choose between primary and accessory for each exercise."
            return render(request, "userprofile/configure.html", setup)

        # all configurations passed! Now build up the complete workout.
        else:
            """ Global variables for a macrocycle """
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
                exercise_1 = selected_exercises(first_max_exercise[day], first_sec_exercise[day])
                exercise_2 = selected_exercises(second_max_exercise[day], second_sec_exercise[day])
                exercise_3 = selected_exercises(third_max_exercise[day], third_sec_exercise[day])
                exercise_4 = selected_exercises(fourth_max_exercise[day], fourth_sec_exercise[day])

                cycle = WorkoutPlan(
                    user_id = request.user,
                    cycle_name = cycle_name,
                    week_count = week_count,
                    day_count = day_count,
                    exercise_1 = exercise_1["exercise"],
                    exercise_1_weight = exercise_1["exercise_weight"],
                    exercise_2 = exercise_2["exercise"], 
                    exercise_2_weight = exercise_2["exercise_weight"],
                    exercise_3 = exercise_3["exercise"], 
                    exercise_3_weight = exercise_3["exercise_weight"],
                    exercise_4 = exercise_4["exercise"], 
                    exercise_4_weight = exercise_4["exercise_weight"],
                    timestamp = timestamp
                    )
                cycle.save()
                day_count += 1

            return render(request, "userprofile/configure.html", {"step_3" : True, "cycle_name" : cycle_name})


def contact(request):
    return render(request, "userprofile/contact.html")


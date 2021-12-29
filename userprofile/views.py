from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.utils import timezone
from datetime import date

#user creation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# database tables
from .models import MaxValue, Exercise_Pool, musclegroups, WorkoutPlan
from .forms import CreateMaxValue, Exercise_Pool_Form, ConfigureWorkout, AchievedReps
from .helpers import epley, check_input, workout_validator, workout_configurator, selected_exercises

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

@login_required
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
    all_cycles = list(set([int(cycle.cycle_name[5:]) for cycle in workout]))
    current_cycle = "cycle" + str(max(all_cycles) )

    # filters model to only contain unique cycle+timestamp combinations
    cycles = WorkoutPlan.objects.filter(user_id=request.user).values("cycle_name", "timestamp").order_by("-timestamp").distinct()

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
        Exercise_Pool.objects.get(id = request.POST["deleted_exercise"]).delete()
        return redirect("profile")

    elif "modified_exercise" in request.POST:
        print(request.POST)
        form_modify_exercise = Exercise_Pool.objects.get(id = request.POST["modified_exercise"]) # retrieve ID from model
        modified_exercise = Exercise_Pool_Form(request.POST, instance=form_modify_exercise) # create instance of that entry and plug it into the form
        modified_exercise.save() # update the model form based on POST data
        return redirect("profile")


@login_required
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


@login_required
def workout(request, cycle):
    # this is a list of deload weeks, in order to identify them in the template
    weeks = [4, 8, 12, 16]

    if request.method == "GET":
        workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
        created_at = [entry.timestamp for entry in workout]  # retrieves date from current cycle
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle, "weeks" : weeks, "created_at" : created_at[0]})

    elif "workout_done" in request.POST:
        print(request.POST)

        # reminder: 1 entry in WorkoutPlan table = 1 day of training
        todays_workout = get_object_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user, day_count=request.POST["day"])

        achieved_reps = AchievedReps(request.POST, instance=todays_workout)
        save_achieved_reps = achieved_reps.save(commit=False) # this step is important in order to additionally update the boolean value in table
        save_achieved_reps.day_completed = True
        save_achieved_reps.save()

        workout = get_list_or_404(WorkoutPlan, cycle_name=cycle, user_id=request.user) #filter the model based on URL snippet
        created_at = [entry.timestamp for entry in workout]  # retrieves date from current cycle
        return render(request, "userprofile/workout.html", {"workout" : workout, "cycle" : cycle, "weeks" : weeks, "created_at" : created_at[0]})


@login_required
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
            setup["error"] = "Please select exercises!"
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

            # every week the weights for primary exercises go up
            weight_max = [0.70, 0.75, 0.80, 0.80, 0.75, 0.80, 0.85, 0.85, 0.80, 0.85, 0.90, 0.90, 0.85, 0.90, 0.95, 0.50]
            weight_max_pointer = 0

            # every mesocycle the weights for secondary exercises go up
            weight_sec = ["high", "mid", "mid", "low"]
            weight_sec_pointer = 0
            """ ------------------------------- """
            
            for month in range(4):
            # loop over entire macrocycle
                for week in range(4):
                # loop over 1 month, which is one mesocycle
                    for day in range(days):
                    # loop over 1 week, which is one microcycle
                        # Currently, POST data is stored in a list. Each index = 1 day
                        exercise_1 = selected_exercises(first_max_exercise[day], first_sec_exercise[day], weight_max[weight_max_pointer], weight_sec[weight_sec_pointer])
                        exercise_2 = selected_exercises(second_max_exercise[day], second_sec_exercise[day], weight_max[weight_max_pointer], weight_sec[weight_sec_pointer])
                        exercise_3 = selected_exercises(third_max_exercise[day], third_sec_exercise[day], weight_max[weight_max_pointer], weight_sec[weight_sec_pointer])
                        exercise_4 = selected_exercises(fourth_max_exercise[day], fourth_sec_exercise[day], weight_max[weight_max_pointer], weight_sec[weight_sec_pointer])

                        cycle = WorkoutPlan(
                            user_id = request.user,
                            cycle_name = cycle_name,
                            week_count = week_count,
                            day_count = day_count,
                            max_weight_percentage = int(weight_max[weight_max_pointer] * 100),
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
                
                    # inner loop is over = 1 week of workouts
                    week_count += 1
                    weight_max_pointer += 1

                # this loop is over = 1 month of workouts
                weight_sec_pointer += 1

            return success(request, cycle_name)
            # return render(request, "userprofile/success.html", {"cycle_name" : cycle_name})

@login_required
def success(request, cycle_name=False):
    return render(request, "userprofile/success.html", {"cycle_name" : cycle_name})

def contact(request):
    return render(request, "userprofile/contact.html")


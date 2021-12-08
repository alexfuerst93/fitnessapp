from django.shortcuts import render, redirect

#user creation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# database tables
from .models import MaxValue, Exercise_Pool
from .forms import CreateExercise, musclegroups, CreateMaxValue, dropdown_exercises

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
    #form
    add_exercise = CreateExercise()
    form_maxval = CreateMaxValue()
    

    sorted_musclegroups = [choice[0] for choice in musclegroups]
    sorted_musclegroups.sort()

    if request.method == "GET":
        wups = []
        for val in max_vals:
            wups.append(val.exercise)
        print(wups)
        return render(request, "userprofile/profile.html", {"maxvals" : max_vals, "exercises" : exercises, "form" : add_exercise, "form_maxval" : form_maxval, "musclegroups" : sorted_musclegroups})

    elif "calculated_maxrep" in request.POST:
        # form validations are missing
        weight = float(request.POST["weight"])
        reps = float(request.POST["reps"])
        result = int(round(0.033 * reps * weight + weight, 0))
        return render(request, "userprofile/profile.html", {"ergebnis" : f"Your Max value: {result}", "form" : add_exercise, "form_maxval" : form_maxval, "musclegroups" : sorted_musclegroups})

    elif "calculate_and_safe" in request.POST:
        print(request.POST)
        # if form_maxval.is_valid(): # why isnt the form validating?
        if request.POST["choose_exercise"] == "0" and request.POST["create_exercise"] == "":
            return render(request, "userprofile/startpage.html")
        elif request.POST["choose_exercise"] != "0" and request.POST["create_exercise"] != "":
            return render(request, "userprofile/startpage.html")
        else:
            weight = float(request.POST["weight"])
            reps = float(request.POST["reps"])
            result = int(round(0.033 * reps * weight + weight, 0))
            max_vals.create(user_id=request.user, exercise=request.POST["create_exercise"], max_value=result)
            return render(request, "userprofile/profile.html", {"maxvals" : max_vals, "ergebnis" : f"Your new Max value for {request.POST['create_exercise']} is: {result}", "form" : add_exercise, "form_maxval" : form_maxval, "musclegroups" : sorted_musclegroups})

    elif "added_exercise" in request.POST:
        # what if the user wants to add 2 identical exercises?
        check = request.POST.get("track", False)
        if check:
            exercises.create(user_id=request.user, title=request.POST["name_of_exercise"], muscle=request.POST["muscle"], track_perform="yes")
        else:
            exercises.create(user_id=request.user, title=request.POST["name_of_exercise"], muscle=request.POST["muscle"], track_perform="no")
        return render(request, "userprofile/profile.html", {"exercises" : exercises, "form" : add_exercise, "musclegroups" : sorted_musclegroups})





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

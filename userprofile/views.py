from django.shortcuts import render, redirect

#user creation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# database tables
from .models import Exercise_Pool
from .forms import CreateExercise

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
    exercises = Exercise_Pool.objects.all() #database
    add_exercise = CreateExercise() #form
    
    if request.method == "GET":
        return render(request, "userprofile/profile.html", {"exercises" : exercises, "form" : add_exercise})

    elif "calculated_maxrep" in request.POST:
        # form validations are missing
        weight = float(request.POST["weight"])
        reps = float(request.POST["reps"])
        result = int(round(0.033 * reps * weight + weight, 0))
        return render(request, "userprofile/profile.html", {"ergebnis" : f"Your Max value: {result}", "form" : add_exercise})

    elif "calculate_and_safe" in request.POST:
        # send to database "MaxValue"
        pass

    elif "added_exercise" in request.POST:
        print(request.POST)
        if request.POST["track"]: #bug
            exercises.create(user_id=request.user, title=request.POST["name_of_exercise"], muscle=request.POST["muscle"], track_perform="yes")
        else:
            exercises.create(user_id=request.user, title=request.POST["name_of_exercise"], muscle=request.POST["muscle"], track_perform="no")
        return render(request, "userprofile/profile.html", {"exercises" : exercises, "form" : add_exercise})

        # def calc(reps, weight):
            # LET DJANGO DO FORM VALIDATION
            # numbers are too big (cmon, you are not the mountain, enter a truthful value & way too many reps! keep it below 10 to have a meaningful max rep)
            # not int or dec: put in numbers!
            # only one value is given
            # take care of "." / ","
            # return int(round(0.033 * reps * weight + weight, 0))

# https://docs.djangoproject.com/en/1.11/intro/tutorial04/

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

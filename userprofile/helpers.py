from .forms import ConfigureWorkout
from .models import MaxValue, Exercise_Pool

def epley(weight, reps):
    # calculates a new 1RM value
    return int(round(0.033 * reps * weight + weight, 0))


def check_input(summed_request):
    # summed_request is a list with nested lists inside, corresponding to the selected exercises
    # loops through the request, checking that at least 1 exercise is selected
    for request in summed_request:
        for val in request:
            if val:
                return True
    return False


def workout_validator(idx, max, sec):
    # this function uses the user-selected days to loop over the index of the user-selected exercises to perform validation
    idx -= 1
    while idx >= 0:
        if max[idx] and sec[idx]:
            return False
        if max[idx] and sec[idx]:
            return False
        if max[idx] and sec[idx]:
            return False
        if max[idx] and sec[idx]:
            return False
        idx -= 1
    return True


def workout_configurator(days):
    # depending on how many days the user wants to workout each week, the following HTML table needs more configuration forms
    # step_1 and step_2 are needed to render the appropriate amount of content on the HTML page
    configure_workout_day1 = ConfigureWorkout()
    configure_workout_day2 = ConfigureWorkout()
    configure_workout_day3 = ConfigureWorkout()
    configure_workout_day4 = ConfigureWorkout()
    configure_workout_day5 = ConfigureWorkout()

    if days == 3:
        return {
            "step_1" : True,
            "step_2" : True,
            "days" : days,
            "configure_workout_day1" : configure_workout_day1,
            "configure_workout_day2" : configure_workout_day2,
            "configure_workout_day3" : configure_workout_day3
        }

    elif days == 4:
        return {
            "step_1" : True,
            "step_2" : True,
            "days" : days,
            "configure_workout_day1" : configure_workout_day1,
            "configure_workout_day2" : configure_workout_day2,
            "configure_workout_day3" : configure_workout_day3,
            "configure_workout_day4" : configure_workout_day4
        }

    else: # days == 5
        return {
            "step_1" : True,
            "step_2" : True,
            "days" : days,
            "configure_workout_day1" : configure_workout_day1,
            "configure_workout_day2" : configure_workout_day2,
            "configure_workout_day3" : configure_workout_day3,
            "configure_workout_day4" : configure_workout_day4,
            "configure_workout_day5" : configure_workout_day5
        }


def selected_exercises(max, sec, weight_max, weight_sec):
    # Determine whether the user selected a max exercise or a secondary exercise per row per day
    # Using the primary key from POST, search for the selected exercise in the corresponding table/model
    if max:
        exercise = MaxValue.objects.get(pk = max)
        return {"exercise" : exercise.exercise, "exercise_weight" : float(exercise.max_value)*weight_max}
    elif sec:
        exercise = Exercise_Pool.objects.get(pk = sec)
        if weight_sec == "high":
            return {"exercise" : exercise.title, "exercise_weight" : exercise.high_range}
        elif weight_sec == "mid":
            return {"exercise" : exercise.title, "exercise_weight" : exercise.mid_range}
        else: # weight_sec == "low"
            return {"exercise" : exercise.title, "exercise_weight" : exercise.low_range}
    else:
        return {"exercise" : "", "exercise_weight" : 0.00}

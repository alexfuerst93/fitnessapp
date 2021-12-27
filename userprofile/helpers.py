from .forms import ConfigureWorkout

def epley(weight, reps):
    # calculates a new 1RM value
    return int(round(0.033 * reps * weight + weight, 0))


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
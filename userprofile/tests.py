from django.test import TestCase

# Create your tests here.
# https://docs.djangoproject.com/en/3.2/intro/tutorial05/

previous_cycles = ["cycle1", "cycle2", "cycle2", "cycle3"]
retrieve_unique_cycles = list(set([int(cycle[5:]) for cycle in previous_cycles]))
cycle_name = "cycle" + str(max(retrieve_unique_cycles) + 1)
print(cycle_name)
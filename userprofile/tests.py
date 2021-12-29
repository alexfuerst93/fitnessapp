from django.test import TestCase

# Create your tests here.
# https://docs.djangoproject.com/en/3.2/intro/tutorial05/

# test_list = [["","",None], [None,"",""]]
# if any(test_list):
#     print("truthy")
# else:
#     print("false")

# test_list = ["", "", ""]
# print(test_list)
# print(test_list[0])

test_list = ["cycle3", "cycle10"]
find_highest = max(test_list)
print(find_highest)
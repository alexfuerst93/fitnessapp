from django.test import TestCase

# Create your tests here.
# https://docs.djangoproject.com/en/3.2/intro/tutorial05/

test_list = [["","",None], [None,"",""]]
if any(test_list):
    print("truthy")
else:
    print("false")
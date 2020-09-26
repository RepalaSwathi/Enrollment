# from django.contrib.auth.models import Student
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from student.models import Student
import random
import string
import requests

def random_string_generator(size, type=None):
	if type == "char":
		chars = chars = string.ascii_uppercase + string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))

def random_mobile_generator():
	first = str(random.randint(600, 999))
	second = str(random.randint(1, 888))
	last = (str(random.randint(1, 9998)).zfill(4))
	return '{}{}{}'.format(first, second, last)

def random_email(y):
	   return ''.join(random.choice(string.ascii_letters) for x in range(y))


class Command(BaseCommand):
	help = 'Create random students'

	def add_arguments(self, parser):
		parser.add_argument('total', type=int, help='Indicates the number of students to be created')

	def handle(self, **kwargs):
		total = kwargs['total']
		gender_choise = ['Female', 'Male']
		for i in range(total):
		 	mobile=random_mobile_generator()
			try:
				student_obj = Student.objects.get(mobile=mobile)
				print "already exist"
			except Student.DoesNotExist as e:
				student_data ={
					"firstname":random_string_generator(10, 'char'),
					"lastname":random_string_generator(10, 'char'), 
					"email":random_email(7)+"@gmail.com",
					"age":random.randint(1, 100),
					"mobile":mobile,
					"gender":random.choice(gender_choise)
					}
				student_obj = Student.objects.create(**student_data)
				print student_data
			except Exception as e:
				print(str(e))
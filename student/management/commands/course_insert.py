from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from student.models import Course
import random
import string

class Command(BaseCommand):
	help = 'Create random courses'

	def add_arguments(self, parser):
		parser.add_argument('total', type=int, help='Indicates the number of course to be created')

	def handle(self, **kwargs):
		total = kwargs['total']
		course_list = ['Java', 'Python', 'DotNet','Networking','WEB','PHP','Angular']
		duration = ['6 months','8 months','12 months']
		category = ['Webtechnology','Mobiletechnology','Networktechnology']
		for i in range(total):
			course_name = random.choice(course_list)
			try:
				course_obj = Course.objects.get(course_name=course_name)
				print "already exist"
			except Course.DoesNotExist as e:
				course_data ={
					"course_name":course_name,
					"course_fee":random.randint(2000, 10000),
					"duration":random.choice(duration),
					"category":random.choice(category)
					}
				cour_obj = Course.objects.create(**course_data)
				print course_data
			except Exception as e:
				print(str(e))
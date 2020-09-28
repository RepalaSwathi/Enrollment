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
		course_list = ['Java', 'Python', 'DotNet']
		duration = ['6 months','8 months','12 months']
		for i in range(total):
			Course.objects.create(
				course_name=random.choice(course_list),
				course_fee=random.randint(2000, 10000),
				duration=random.choice(duration))
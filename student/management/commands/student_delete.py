from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from student.models import Student

class Command(BaseCommand):
    help = 'delete specific student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', nargs='+', type=int)

    def handle(self, **options):
        for student_id in options['student_id']:
            try:
                student = Student.objects.get(pk=student_id).delete()
            except Student.DoesNotExist:
                print('student does not exist')

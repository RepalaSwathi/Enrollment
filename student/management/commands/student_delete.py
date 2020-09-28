from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from student.models import Student

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('student_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for student_id in options['student_id']:
            try:
                student = Student.objects.get(pk=student_id).delete()
            except Student.DoesNotExist:
                print('student does not exist')

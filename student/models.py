from django.db import models
import re

GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
)

STATUS_CHOICES = ( 
    ("accepted", "accepted"), 
    ("rejected", "rejected"), 
    ("under progressive", "under progressive"), 
) 

# Create your models here.
class Course(models.Model):
	course_name = models.CharField(max_length=200)
	duration = models.CharField(max_length=50)
	course_fee = models.CharField(max_length=40)

	

class Student(models.Model):
	
	firstname = models.CharField(max_length=100,blank=True,null=True)
	lastname = models.CharField(max_length=100,blank=True,null=True)
	mobile = models.CharField(max_length=10,blank=True,null=True)
	gender = models.CharField(max_length=20,choices = GENDER_CHOICES)
	email = models.CharField(max_length=40,blank=True,null=True)
	age = models.IntegerField()

	

class StudentCourse(models.Model):
	student = models.ForeignKey(Student)
	course = models.ForeignKey(Course)
	status = models.CharField(max_length = 20,choices = STATUS_CHOICES)
	enroll_date = models.DateField(auto_now=True)

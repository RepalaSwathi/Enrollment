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
	category = models.CharField(max_length=20)

	

class Student(models.Model):
	
	firstname = models.CharField(max_length=100,blank=True,null=True)
	lastname = models.CharField(max_length=100,blank=True,null=True)
	mobile = models.CharField(max_length=20,blank=True,null=True)
	gender = models.CharField(max_length=20,choices = GENDER_CHOICES)
	email = models.CharField(max_length=40,blank=True,null=True)
	age = models.IntegerField()

	

class StudentCourse(models.Model):
	student = models.ForeignKey(Student)
	course = models.ForeignKey(Course)
	status = models.CharField(max_length = 20,choices = STATUS_CHOICES)
	enroll_date = models.DateField(auto_now=True)


class Organization(models.Model):
    org_name = models.CharField(max_length=200, null=True, blank=True)
    org_email = models.CharField(max_length=20, null=20, blank=True)
    org_address = models.CharField(max_length=200, null=True, blank=True)
    org_mobile = models.CharField(max_length=20, null=20, blank=True)

class OrganizationCourse(models.Model):
	organization = models.ForeignKey(Organization)
	course = models.ForeignKey(Course)
	student = models.ForeignKey(Student)
	



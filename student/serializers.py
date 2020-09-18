from student.serializers import *
from rest_framework import serializers
from student.models import *
import re

class StudentSerializer(serializers.Serializer):
	firstname = serializers.CharField(max_length=100)
	lastname = serializers.CharField(max_length=100)
	email = serializers.CharField(max_length=40)   
	age = serializers.IntegerField()  
	gender = serializers.CharField(max_length=20)
	mobile = serializers.CharField(max_length=250)

	def validate_firstname(self, value):
		if len(value) > 20:
			raise serializers.ValidationError("Name Should Not Be More Than 20 Character")
		if not value.isalpha():
			raise serializers.ValidationError("Name Should Contains Character Only")
					
	def validate_lastname(self, value):
		if len(value) > 20:
				raise serializers.ValidationError("Name Should Not Be More Than 20 Character")
		if not value.isalpha():
				raise serializers.ValidationError("Name Should Contains Character Only")


class CourseSerializer(serializers.Serializer):
	course_name = serializers.CharField(max_length=200)
	duration = serializers.CharField(max_length=50)
	course_fee = serializers.CharField(max_length=40)

	def validate_course_name(self, value):
		if len(value) > 20:
				raise serializers.ValidationError("Name Should Not Be More Than 20 Character")
		if not value.isalpha():
				raise serializers.ValidationError("Name Should Contains Character Only")


class UpdateSerializer(serializers.Serializer):
	status = serializers.CharField(max_length = 20)

class StudentGetSerializer(serializers.Serializer):
	ack_number = serializers.CharField(max_length=100)
    

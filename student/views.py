from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from student.models import *
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import viewsets
from student.serializers import StudentSerializer
from student.serializers import CourseSerializer
from student.serializers import UpdateSerializer
from student.serializers import StudentGetSerializer
from rest_framework.response import Response 
from django.http import HttpResponse,Http404
from django.http import HttpResponse
from rest_framework.response import Response 
from . import serializers
import logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from rest_framework import viewsets
from rest_framework import status
import csv
# import datetime
from datetime import datetime
# Create your views here.

class StudentRegister(APIView):
	def post(self,request,format=None):
		logger.info("*** Student POST Request Process Start ***")
		serializer = StudentSerializer(data=request.data)
		if serializer.is_valid():
			try:
				try:
					st_obj = StudentCourse.objects.get(student__firstname=request.data['firstname'],course__course_name=request.data['course_name'])
					context_data = {"success" : False, "data" :{"message" : "You Have Already Enrolled "}}
					return Response(context_data)
				except Exception as e:
					print(str(e))
				course_obj = Course.objects.get(course_name=request.data.get('course_name'))
				student_data={
						"firstname":request.data.get('firstname'),
						"lastname": request.data.get('lastname'),
						"email": request.data.get('email'),
						"age": request.data.get('age'),
						"mobile": request.data.get('mobile'),
						"gender": request.data.get('gender',''),
					}
				mobile = request.data['mobile']
				if not mobile.startswith(('6','7','8','9')):
					context_data = {"success" : False, "errors" :{"message" : "Invalid mobile number"}}
					return Response((context_data)) 
				try:
					student_obj = Student.objects.get(firstname=request.data['firstname'])
				except Student.DoesNotExist as e:
					student_obj = Student.objects.create(**student_data)
				except Exception as e:
					print(str(e))
				sc_obj = StudentCourse.objects.create(student=student_obj,course=course_obj)
				context_data = {"success" : True, "data" : {"student_data":student_data,"Acknowledgement_Number":sc_obj.pk,"message" : " Student Enrolled Successfully"} }
			except Exception as e:
				print(e)
				context_data = {"success" : False, "data" : {"message":str(e) }}
				return Response(context_data)
		else:
			print serializer.errors
			context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
		logger.info("*** Student POST Request Process End ***")
		return Response(context_data)
class StudentViewSet(APIView):
	def post(self,request,query_type,format=None): 
		# logger.info("StudentListViewSet request data:{0}")
		# serializer = StudentGetSerializer(data=request.data)
		# if serializer.is_valid():
		if query_type == 'get':
			try:
				print("hiii")
				student_obj = StudentCourse.objects.get(pk=request.data['ack_number'])
				student_data = []
				stu_obj ={
						"firstname":student_obj.student.firstname,
						"lastname":student_obj.student.lastname,
						"email":student_obj.student.email,
						"mobile":student_obj.student.mobile,
						"age":student_obj.student.age,
						"gender":student_obj.student.gender,
						"status":student_obj.status,
						"course":student_obj.course.course_name,
						"course_fee":student_obj.course.course_fee,
						"duration":student_obj.course.duration,
						"Acknowledgement_Number":student_obj.id,
						}
				student_data.append(stu_obj)
				context_data = {"success" : True, "data" :{"student_data" :student_data}}
			except Student.DoesNotExist as e:            
				context_data = {"success" : False, "errors" : {"message":"No Student Record Found on This Acknowledgement_Number"}}
			except Exception as e:
				print(str(e))
		
		elif query_type == 'csv':
			print("helo csv")
			start_date = request.data['start_date']
			end_date = request.data['end_date']
			student_obj_list =StudentCourse.objects.filter(enroll_date__range=[start_date,end_date])
			student_data = []
			for each_student_obj in student_obj_list:
				stu_obj ={
					"firstname":each_student_obj.student.firstname,
					"lastname":each_student_obj.student.lastname,
					"email":each_student_obj.student.email,
					"mobile":each_student_obj.student.mobile,
					"age":each_student_obj.student.age,
					"gender":each_student_obj.student.gender,
					"status":each_student_obj.status,
					"course":each_student_obj.course.course_name,
					"course_fee":each_student_obj.course.course_fee,
					"duration":each_student_obj.course.duration,
					"Acknowledgement_Number":each_student_obj.id,
							
					}
				student_data.append(stu_obj)
			print student_data,"st_obj"
			response = HttpResponse(content_type='text/csv')
			current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
			filename = "StudentViewSet-Download_{0}.csv".format(current_date)
			response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
			fieldnames = ['Status', 'Course fee','Duration','Course Name','First Name','Lastname','Age','Email','Mobile','Ackn_Number']
			writer = csv.writer(response)
			writer.writerow(fieldnames)
			writer.writerow([student_data])
			return response 
		else:
			context_data = {"success" : False,"errors" : {"message":"Invalid Query"}}
		return Response(context_data) 
		# else:
		# 	print serializer.errors
		# 	context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
		# 	logger.info("*** StudentViewSet Request Process End ***")  
		# 	return Response(context_data)

class StudentDelete(APIView):
	def post(self,request,format=None,pk=None):
			logger.info("*** StudentDelete  Request Process Start ***")
			try:
				stuc_obj = StudentCourse.objects.get(pk=request.data['id'])
				stuc_obj.delete()     
				context_data = {"success" : True, "data" :{"message":"studen record has been deleted"}} 
			except StudentCourse.DoesNotExist as e:            
				context_data = {"success" : False, "errors" : {"message":"No Student Record Found on this id"}}
				pass
			logger.info("*** StudentDelete Request Process End ***")  
			return Response(context_data)

class CourseCreate(APIView):
	def post(self,request,format=None):
		logger.info("*** CourseCreate POST Request Process Start ***")	
		serializer = CourseSerializer(data=request.data)
		if serializer.is_valid():
			course_obj = Course.objects.filter(course_name=request.data['course_name'])
			if course_obj.count() > 0:
				context_data = {"success" : False, "data" :{"message" : "Course already Exist"}}
				return Response(context_data)
			try:
				course_obj={
							"course_name":request.data.get('course_name'),
							"duration": request.data.get('duration'),
							"course_fee": request.data.get('course_fee'),
							}
				course_data = Course.objects.create(**course_obj)
				queryset = Course.objects.filter(course_name=request.data['course_name'])
				course_obj_list = queryset.values('course_name','duration','course_fee')				
				context_data = {"success" : True, "data" : {"course_data" :course_obj_list, "message" : " Course Created Successfully"}}
				return Response(context_data)
			except Exception as e:
				print(e)
				pass
		else:
			print serializer.errors
			context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
			logger.info("*** CourseCreate Request Process End ***")  
		return Response(context_data)

class StatusUpdate(APIView):
	def post(self,request,format=None,pk=None):
		serializer = UpdateSerializer(data=request.data)
		if serializer.is_valid():
			try:
				stu_obj = StudentCourse.objects.filter(pk=pk)
				student_data = {
				"status":request.data.get('status','').lower()
				}
				stu_obj.update(**student_data)     
				context_data = {"success" : True, "data" :{"message":"status updated"}}
				return Response(context_data) 
			except Exception as e:
				context_data = {"success" : False, "errors" : {"message":str(e)}}
				pass
			return Response(context_data)       
		else:
			print serializer.errors
			context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
		return Response(context_data)
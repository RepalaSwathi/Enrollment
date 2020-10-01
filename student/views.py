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
from student.serializers import OrganizationAddSerializer
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
from django.db.models import Count,Max,Min
import csv
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
				org_obj = Organization.objects.get(org_name=request.data.get('org_name'))
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
				organization_obj = OrganizationCourse.objects.create(organization=org_obj,course=course_obj,student=student_obj)
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
class StudentGet(APIView):
	def get(self,request,pk=None):
		try:
			student_list =[]
			student_obj =StudentCourse.objects.get(pk=pk)
			st_form={
			"status":student_obj.status,
			"firstname":student_obj.student.firstname,
			"lastname":student_obj.student.lastname,
			"email": student_obj.student.email,
			"gender":student_obj.student.gender,
			"age":student_obj.student.age,
			"mobile":student_obj.student.mobile,
			"course_name":student_obj.course.course_name,
			"course_fee": student_obj.course.course_fee,
			"duration":student_obj.course.duration,
			}
			student_list.append(st_form)		
			print student_list
			context_data = {"success" : True, "data" :{"student_data" :student_list}}
			return Response(context_data)
		except Student.DoesNotExist as e:            
			context_data = {"success" : False, "errors" : {"message":"No Student Record Found on This Acknowledgement_Number"}}
		except Exception as e:
			print(str(e))
			context_data = {"success" : False, "data" : {"message":str(e) }}
			return Response(context_data)

class StudentDelete(APIView):
	def post(self,request,format=None,pk=None):
			logger.info("*** StudentDelete  Request Process Start ***")
			try:
				stuc_obj = StudentCourse.objects.get(pk=request.data['id'])
				stuc_obj.delete()     
				context_data = {"success" : True, "data" :{"message":"student record has been deleted"}} 
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
							"category": request.data.get('category'),
							}
				course_data = Course.objects.create(**course_obj)
				queryset = Course.objects.filter(course_name=request.data['course_name'])
				course_obj_list = queryset.values('course_name','duration','course_fee','category')				
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

# class Summary(APIView):
# 	def post(self,request,format=None):
# 		try:
# 			queryset=StudentCourse.objects.filter(enroll_date=request.data['date']).count()
# 			context_data = {"success" : True, "data" : {"Number of students enrolled " :queryset}}
# 			return Response(context_data)
# 		except Exception as e:
# 			print(e)
# 			pass
# 		try:
# 			queryset=StudentCourse.objects.filter(course__course_name=request.data['course_name'])
# 			context_data = {"success" : True, "data" : {"Number of students enrolled on this course" :queryset.count()}}
# 			return Response(context_data)
# 		except Exception as e:
# 			print(e)
# 			pass

class Aggregate(APIView):
	def get(self,request,query_type):
		if query_type == 'Max':
			try:
				sc_obj=StudentCourse.objects.aggregate(Max('course__course_name'))
				context_data = {"success" : True, "data" : {"data":sc_obj,"message" : "Maximum registered course"}}
				return Response(context_data)
			except Exception as e:
				print(e)
				pass
		elif query_type == 'Min':
			try:
				sc_obj=StudentCourse.objects.aggregate(Min('course__course_name'))
				context_data = {"success" : True, "data" : {"data" :sc_obj, "message" : "Manimum registered course"}}
				return Response(context_data)
			except Exception as e:
				print(e)
				pass
		else:
			context_data = {"success" : False,"errors" : {"message":"Invalid Query"}}
		return Response(context_data)

class StudentListViewSet(APIView):
	def get(self,request,query_type): 
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		print start_date,end_date
		if query_type == 'json':
			try:
				student_list =[]
				student_obj_list =StudentCourse.objects.filter(enroll_date__range=[start_date,end_date])
				for each_doc in student_obj_list:
					st_form={
					"id":each_doc.id,
					"status":each_doc.status,
					"firstname":each_doc.student.firstname,
					"lastname":each_doc.student.lastname,
					"email": each_doc.student.email,
					"gender":each_doc.student.gender,
					"age":each_doc.student.age,
					"mobile":each_doc.student.mobile,
					"course_name":each_doc.course.course_name,
					"course_fee": each_doc.course.course_fee,
					"duration":each_doc.course.duration,
					}
					student_list.append(st_form)		
				context_data = {"success" : True, "data" :{"student_data" :student_list}}
				return Response(context_data)
			except Exception as e:
				print(str(e))
				context_data = {"success" : False, "data" : {"message":str(e) }}
				return Response(context_data)
		
		elif query_type == 'csv':
			print("helo csv")
			start_date = request.GET.get('start_date')
			end_date = request.GET.get('end_date')
			student_list =[]
			student_obj_list =StudentCourse.objects.filter(enroll_date__range=[start_date,end_date])
			for each_doc in student_obj_list:
				id = each_doc.id
				status = each_doc.status
				firstname = each_doc.student.firstname
				lastname = each_doc.student.lastname
				email = each_doc.student.email
				gender = each_doc.student.gender
				age = each_doc.student.age
				mobile = each_doc.student.mobile
				course_name = each_doc.course.course_name
				course_fee = each_doc.course.course_fee
				duration = each_doc.course.duration
				student_list.append([status,course_fee,duration,course_name,firstname,lastname,age,email,gender,mobile,id])
			response = HttpResponse(content_type='text/csv')
			current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
			filename = "StudentViewSet-Download_{0}.csv".format(current_date)
			response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
			fieldnames = ['Status', 'Course fee','Duration','Course Name','First Name','Lastname','Age','Email','Gender','Mobile','Ackn_Number']
			writer = csv.writer(response)
			writer.writerow(fieldnames)
			writer.writerows(student_list)
			return response 
		else:
			context_data = {"success" : False,"errors" : {"message":"Invalid Query"}}
			return Response(context_data) 
class Summary(APIView):
	def get(self,request,query_type):
		if query_type == 'total_registrations':
			try:
				enroll_date = request.GET.get('enroll_date')
				print enroll_date
				student_list =[]
				student_obj_list =StudentCourse.objects.filter(enroll_date=(enroll_date))
				print student_obj_list
				for each_doc in student_obj_list:
					id = each_doc.id
					status = each_doc.status
					firstname = each_doc.student.firstname
					lastname = each_doc.student.lastname
					email = each_doc.student.email
					gender = each_doc.student.gender
					age = each_doc.student.age
					mobile = each_doc.student.mobile
					course_name = each_doc.course.course_name
					course_fee = each_doc.course.course_fee
					duration = each_doc.course.duration
					student_list.append([status,course_fee,duration,course_name,firstname,lastname,age,email,gender,mobile,id])
				response = HttpResponse(content_type='text/csv')
				current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
				filename = "StudentViewSet-Download_{0}.csv".format(current_date)
				response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
				fieldnames = ['Status', 'Course fee','Duration','Course Name','First Name','Lastname','Age','Email','Gender','Mobile','Ackn_Number']
				writer = csv.writer(response)
				writer.writerow(fieldnames)
				writer.writerows(student_list)
				return response 
			except Exception as e:
				print(str(e))
				context_data = {"success" : False, "data" : {"message":str(e) }}
				return Response(context_data)
		elif query_type == 'total_courseregister':
			try:
				course_name = request.GET.get('course_name')
				student_list =[]
				student_obj_list =StudentCourse.objects.filter(course__course_name=(course_name))
				for each_doc in student_obj_list:
					id = each_doc.id
					status = each_doc.status
					firstname = each_doc.student.firstname
					lastname = each_doc.student.lastname
					email = each_doc.student.email
					gender = each_doc.student.gender
					age = each_doc.student.age
					mobile = each_doc.student.mobile
					course_name = each_doc.course.course_name
					course_fee = each_doc.course.course_fee
					duration = each_doc.course.duration
					student_list.append([status,course_fee,duration,course_name,firstname,lastname,age,email,gender,mobile,id])
				response = HttpResponse(content_type='text/csv')
				current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
				filename = "StudentViewSet-Download_{0}.csv".format(current_date)
				response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
				fieldnames = ['Status', 'Course fee','Duration','Course Name','First Name','Lastname','Age','Email','Gender','Mobile','Ackn_Number']
				writer = csv.writer(response)
				writer.writerow(fieldnames)
				writer.writerows(student_list)
				return response 
			except Exception as e:
				print(str(e))
				context_data = {"success" : False, "data" : {"message":str(e) }}
				return Response(context_data)
		elif query_type == 'last_transactions':
			try:
				enroll_date = request.GET.get('enroll_date')
				student_list =[]
				student_obj_list =StudentCourse.objects.filter(enroll_date=(enroll_date)).order_by('-id')[:10]
				for each_doc in student_obj_list:
					id =each_doc.id
					status = each_doc.status
					firstname = each_doc.student.firstname
					lastname = each_doc.student.lastname
					email = each_doc.student.email
					gender = each_doc.student.gender
					age = each_doc.student.age
					mobile = each_doc.student.mobile
					course_name = each_doc.course.course_name
					course_fee = each_doc.course.course_fee
					duration = each_doc.course.duration
					student_list.append([status,course_fee,duration,course_name,firstname,lastname,age,email,gender,mobile,id])
				response = HttpResponse(content_type='text/csv')
				current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
				filename = "StudentViewSet-Download_{0}.csv".format(current_date)
				response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
				fieldnames = ['Status', 'Course fee','Duration','Course Name','First Name','Lastname','Age','Email','Gender','Mobile','Ackn_Number']
				writer = csv.writer(response)
				writer.writerow(fieldnames)
				writer.writerows(student_list)
				return response 
			except Exception as e:
				print(str(e))
				context_data = {"success" : False, "data" : {"message":str(e) }}
				return Response(context_data)
		else:
			context_data = {"success" : False,"errors" : {"message":"Invalid Query"}}
			return Response(context_data)

class OrganizationAdd(APIView):
	def post(self,request,format=None):
		logger.info("*** OrganizationAdd POST Request Process Start ***")	
		serializer = OrganizationAddSerializer(data=request.data)
		if serializer.is_valid():
			org_obj = Organization.objects.filter(org_name=request.data['org_name'])
			if org_obj.count() > 0:
				context_data = {"success" : False, "data" :{"message" : "Organization already Exist"}}
				return Response(context_data)
			try:
				# course_obj = Course.objects.get(course_name=request.data.get('course_name'))
				org_data={
							"org_name":request.data.get('org_name'),
							"org_email": request.data.get('org_email'),
							"org_address": request.data.get('org_address'),
							"org_mobile": request.data.get('org_mobile'),
							}
				org_obj = Organization.objects.create(**org_data)
				queryset = Organization.objects.filter(org_name=request.data['org_name'])
				org_obj_list = queryset.values('org_name','org_mobile','org_email','org_address')
				# or_obj = OrganizationCourse.objects.create(course=course_obj,organization=org_obj)				
				context_data = {"success" : True, "data" : {"organization_data" :org_obj_list, "message" : " Organization Added Successfully"}}
				return Response(context_data)
			except Exception as e:
				print(e)
				pass
		else:
			print serializer.errors
			context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
			logger.info("*** OrganizationAdd Request Process End ***")  
			return Response(context_data)

class OrganizationCourseGet(APIView):
	def get(self,request,pk=None):
		try:
			org_list =[]
			org_obj_list =OrganizationCourse.objects.filter(pk=pk)
			for each_doc in org_obj_list:
				org_form={
					"id":each_doc.id,
					"firstname":each_doc.student.firstname,
					"lastname":each_doc.student.lastname,
					"email": each_doc.student.email,
					"gender":each_doc.student.gender,
					"age":each_doc.student.age,
					"mobile":each_doc.student.mobile,
					"course_name":each_doc.course.course_name,
					"course_fee": each_doc.course.course_fee,
					"category":each_doc.course.category,
					"duration":each_doc.course.duration,
					"org_name":each_doc.organization.org_name,
					"org_email":each_doc.organization.org_email,

					}
				org_list.append(org_form)		
			context_data = {"success" : True, "data" :{"organization_data" :org_list}}
			return Response(context_data)
		except Exception as e:
			print(str(e))
			context_data = {"success" : False, "data" : {"message":str(e) }}
			return Response(context_data)


class OrganizationCourseCsv(APIView):
	def get(self,request):
		org_name = request.GET.get('org_name')
		org_list =[]
		org_obj_list =OrganizationCourse.objects.filter(organization__org_name=(org_name))
		for each_doc in org_obj_list:
			id = each_doc.id
			firstname = each_doc.student.firstname
			lastname = each_doc.student.lastname
			email = each_doc.student.email
			gender = each_doc.student.gender
			age = each_doc.student.age
			mobile = each_doc.student.mobile
			course_name = each_doc.course.course_name
			course_fee = each_doc.course.course_fee
			duration = each_doc.course.duration
			category = each_doc.course.category
			org_name = each_doc.organization.org_name
			org_mobile = each_doc.organization.org_mobile
			org_email = each_doc.organization.org_email
			org_address = each_doc.organization.org_address
			org_list.append([category,course_fee,duration,course_name,firstname,lastname,age,email,gender,mobile,id,org_name,org_mobile,org_email,org_address])
		response = HttpResponse(content_type='text/csv')
		current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
		filename = "OrganizationViewSet-Download_{0}.csv".format(current_date)
		response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
		fieldnames = ['Category', 'Course fee','Duration','Course Name','First Name','Lastname','Age','Email','Gender','Mobile','Ackn_Number','Organization','orgMobile','orgEmail','orgAddress']
		writer = csv.writer(response)
		writer.writerow(fieldnames)
		writer.writerows(org_list)
		return response 
			
from django.conf.urls import include, url
from student.views import *
# from rest_framework import routers
from . import views

urlpatterns = [
    #Student Enroll And Get,Delete
    url(r'^enroll/student/',StudentRegister.as_view()),
    url(r'^studentview/(?P<query_type>\w+)$',StudentListViewSet.as_view()),
    url(r'^get/(?P<pk>[\w-]+)$',StudentGet.as_view()),
    url(r'^delete/student/',StudentDelete.as_view()),

    url(r'^summary/(?P<query_type>\w+)',Summary.as_view()),
    url(r'^aggre/(?P<query_type>\w+)$',Aggregate.as_view()),

    #Course Add
    url(r'^course/create$',CourseCreate.as_view()),

    #status Update
    url(r'^status/(?P<pk>[\w-]+)/update$',StatusUpdate.as_view()),

    #organization
    url(r'^organization/add',OrganizationAdd.as_view()),
    url(r'^org/get/(?P<pk>[\w-]+)$',OrganizationCourseGet.as_view()),
    url(r'^org/csv/',OrganizationCourseCsv.as_view()),


]

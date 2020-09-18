from django.conf.urls import include, url
from student.views import *
# from rest_framework import routers
from . import views

urlpatterns = [
    #Student Enroll And Get,Delete
    url(r'^enroll/student/',StudentRegister.as_view()),
    url(r'^studentview/(?P<query_type>\w+)$',StudentViewSet.as_view()),
    url(r'^delete/student/',StudentDelete.as_view()),

    #Course Add
    url(r'^course/create$',CourseCreate.as_view()),

    #status Update
    url(r'^status/(?P<pk>[\w-]+)/update$',StatusUpdate.as_view()),

]

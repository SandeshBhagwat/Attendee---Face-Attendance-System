from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('feedback/', views.feedback, name='feedback'),
    path('services/', views.services, name='services'),
    path('students/dashboard/', views.students, name='studentDashboard'),
    path('students/capture/', views.capture, name='capture'),
    path('students/capture/create_dataset/', views.create_dataset, name='create_dataset'),
    path('students/giveattendance/',views.giveAttendance,name='giveAttendance'),
    path('students/attendance/',views.myAttendance,name='myAttendance'),
    path('students/timetable/',views.studentTimetable,name='studentTimetable'),
    path('recognize/', views.recognize, name='recognize'),
    path('teachers/dashboard/', views.teachers, name='teacherDashboard'),
    path('teachers/attendance/',views.takeAttendance,name='takeAttendance'),
    path('teachers/record/',views.record,name='record'),
    path('teachers/timetable/',views.teacherTimetable,name='teacerTimetable'),
 
    # path('students/giveattendance/',views.recognize,name='giveAttendance'),

    
]
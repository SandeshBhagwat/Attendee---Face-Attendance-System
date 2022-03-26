import email
from django.db import models
import datetime


from pytz import timezone

# Create your models here.
class registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254)


class classAttendance(models.Model):
    start_Time=models.TimeField()
    end_Time=models.TimeField()
    date=models.DateField(default=datetime.date.today)
    subject_name=models.CharField(max_length=20)
    make_available_for=models.IntegerField(default=5)
    create_time=models.DateTimeField(default=datetime.datetime.now)
    close_time=models.DateTimeField(default=datetime.datetime.now)
    # status=models.BooleanField(default=False)
    # student_id=models.IntegerField()

class studAttendance(models.Model):
    class_id=models.IntegerField()
    student_id=models.IntegerField()
    status=models.BooleanField(default=False)









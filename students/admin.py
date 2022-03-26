from msilib.schema import AdminUISequence
from django.contrib import admin

# Register your models here.
from .models import classAttendance,registration,studAttendance

class classattendance(admin.ModelAdmin):
    list_display=('id','start_Time','end_Time','date','subject_name','make_available_for','create_time','close_time')
    # list_filter=('date')

class studentattendance(admin.ModelAdmin):
    list_display=('id','student_id','class_id','status')

admin.site.register(classAttendance,classattendance)
admin.site.register(registration)
admin.site.register(studAttendance,studentattendance)

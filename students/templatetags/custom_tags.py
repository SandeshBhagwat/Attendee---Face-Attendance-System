from django import template
from students.models import classAttendance,studAttendance

register = template.Library()

@register.simple_tag
def recognition():

    print("inside template tage")
    return recognition

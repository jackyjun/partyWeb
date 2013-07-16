# Create your views here.
from models import Activity,StudentActivity
from django.shortcuts import render_to_response
from datetime import *

def get_activity(request,id):
    activity = Activity.objects.get(id=id)
    return render_to_response('activity.html',{'activity':activity})

def list_activity(request):
    activity_list = Activity.objects.all()
    activity_dic = {}
    for activity in activity_list:
        if activity.deadline > date.today():
            flag = True
        else:
            flag = False
        activity_dic[activity] = flag
    return render_to_response('activity_list.html',{'activity_dic':activity_dic})

def join_activity(request,id):
    #user = request.user
    studentActivity = StudentActivity(student_id = 1,activity_id = id)
    studentActivity.save()
    return render_to_response('home.html')
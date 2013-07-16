# Create your views here
#coding=utf-8
from models import Activity,StudentActivity,ActivityForm
from member.models import UserStudent
from django.shortcuts import render_to_response,redirect,render
from django.views.decorators.csrf import csrf_exempt
from datetime import *

def get_activity(request,id):
    activity = Activity.objects.get(id=id)
    activity.start_time = activity.start_time.strftime('%Y-%m-%d')
    activity.end_time = activity.end_time.strftime('%Y-%m-%d')
    activity.deadline = activity.deadline.strftime('%Y-%m-%d')
    return render_to_response('activity_detail.html',{'activity':activity})

def list_activity(request):
    user = request.user
    activity_list = Activity.objects.all().order_by('-deadline')
    list = []
    for activity in activity_list:
        activity_dic = {}
        if activity.deadline < date.today():
            flag = -1
        else:
            try:
                if user.is_active:
                    userStudent = UserStudent.objects.get(user = user)
                    student = userStudent.student
                    StudentActivity.objects.get(student_id = student.id,activity_id = activity.id)
                    flag = 1
                else:
                    flag = 0
            except StudentActivity.DoesNotExist:
                flag = 0
        activity.start_time = activity.start_time.strftime('%Y-%m-%d')
        activity.end_time = activity.end_time.strftime('%Y-%m-%d')
        activity.deadline = activity.deadline.strftime('%Y-%m-%d')
        activity_dic[activity] = flag
        list.append(activity_dic)
    return render_to_response('activity_list.html',{'activity_list':list})

def join_activity(request,id):
    user = request.user
    if user.is_active:
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        StudentActivity.objects.get_or_create(student_id = student.id,activity_id = id)
        return redirect(list_activity)
    else:
        return render_to_response('login.html')

def cancel_activity(request,id):
    user = request.user
    if user.is_active:
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        try:
            studentActivity = StudentActivity.objects.get(student_id = student.id,activity_id = id)
            studentActivity.delete()
            return redirect(list_activity)
        except StudentActivity.DoesNotExist:
            return redirect(list_activity)
    else:
        return render_to_response('login.html')

def add_activity(request):
    user = request.user
    if user.is_active:
        if request.method == 'POST':
            form = ActivityForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()
                return render_to_response('home.html')
        else:
            form = ActivityForm()
        return render(request, 'add_activity.html', {
            'form': form,
        })
    else:
        return render_to_response('login.html')

def modify_activity(request,id):
    user = request.user
    activity = Activity.objects.get(id=id)
    if user.is_active:
        if request.method == 'POST':
            form = ActivityForm(request.POST,instance=activity) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()
                return render_to_response('home.html')
        else:
            form = ActivityForm(instance=activity)
        return render(request, 'modify_activity.html', {
            'form': form,
        })
    else:
        return render_to_response('login.html')

def delete_activity(request,id):
    user = request.user
    if user.is_active:
        try:
            activity = Activity.objects.get(id = id)
            activity.delete()
            return redirect(list_activity)
        except Activity.DoesNotExist:
            return redirect(list_activity)
    else:
        return render_to_response('login.html')

@csrf_exempt
def search_activity(request):
    user = request.user
    if user.is_active:
        if request.method=='POST':
            title = request.POST['title']
            type = request.POST['type']
            flag = True
            if int(type)!= -1:
                list = Activity.objects.filter(type=type)
            else:
                list = Activity.objects.all()
            activity_list = []
            for activity in list:
                if title in activity.title:
                    activity.start_time = activity.start_time.strftime('%Y-%m-%d')
                    activity_list.append(activity)
            if len(activity_list)==0:
                flag = False
            context = {
                'activity_list':activity_list,
                'flag':flag,
            }
            return render_to_response('activity_search.html',context)
        else:
            return render_to_response('activity_search.html')
    else:
        return render_to_response('login.html')

def examine_activity(request,id):
    user = request.user
    if user.is_active:
        activity = Activity.objects.get(id = id)
        activity.start_time = activity.start_time.strftime('%Y-%m-%d')
        studentActivity_list = StudentActivity.objects.filter(activity = activity)
        student_dic = {}
        for studentActivity in studentActivity_list:
            student_dic[studentActivity.student] = studentActivity
        context ={
            'activity': activity,
            'student_dic': student_dic,
        }
        print context
        return render_to_response('examine_activity.html',context)
    else:
        return render_to_response('login.html')

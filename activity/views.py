# Create your views here
#coding=utf-8
from models import Activity,StudentActivity,ActivityForm
from member.models import UserStudent,PartyBranch,Student
from django.shortcuts import render_to_response,redirect,render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import *

def get_activity(request,id):
    activity = Activity.objects.get(id=id)
    activity.start_time = activity.start_time.strftime('%Y-%m-%d')
    activity.end_time = activity.end_time.strftime('%Y-%m-%d')
    activity.deadline = activity.deadline.strftime('%Y-%m-%d')
    return render_to_response('activity_detail.html',
                              {
                                'activity':activity,
                                'user':request.user,
                              })

def list_activity(request,type=5):
    choice = Activity.TYPE_CHOICE
    user = request.user
    title = u'活动'
    if type != 5:
        activity_list = Activity.objects.filter(type=type).order_by('-deadline')
        title = choice[int(type)][1]
    else:
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
    return render_to_response('activity_list.html',
                              {
                               'activity_list':list,
                               'title':title,
                               'type':type,
                               'user':request.user,
                              })

@login_required(login_url='/user_login/')
def join_activity(request,type,id):
    user = request.user
    userStudent = UserStudent.objects.get(user = user)
    student = userStudent.student
    try:
        activity = Activity.objects.get(id=id)
        if activity.deadline >= date.today():
            StudentActivity.objects.get_or_create(student_id = student.id,activity_id = id)
        else:
            print("late for deadline,u can't join it.")
    except Activity.DoesNotExist:
        print('activity does not exist')


    return redirect('/list_activity/%s'%type)

@login_required(login_url='/user_login/')
def cancel_activity(request,type,id):
    user = request.user
    userStudent = UserStudent.objects.get(user = user)
    student = userStudent.student
    try:
        studentActivity = StudentActivity.objects.get(student_id = student.id,activity_id = id)
        activity = Activity.objects.get(id=id)
        if activity.deadline >= date.today():
            studentActivity.delete()
        else:
            print('time error')
        return redirect('/list_activity/%s'%type)
    except StudentActivity.DoesNotExist:
        print('activity error')
        return redirect('/list_activity/%s'%type)

@login_required(login_url='/user_login/')
def add_activity(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ActivityForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                activity = form.save(commit=False)
                try:
                    userStudent = UserStudent.objects.get(user = request.user)
                    student = userStudent.student
                    activity.publisher = student.name
                except UserStudent.DoesNotExist:
                    activity.publisher = u'管理员'
                activity.save()
                return render_to_response('activity_search.html',{'user':request.user})
        else:
            form = ActivityForm()
        return render(request, 'add_activity.html', {
            'form': form,
            'user':request.user,
        })
    else:
        return render_to_response('permission_error.html')

@login_required(login_url='/user_login/')
def modify_activity(request,id):
    user = request.user
    activity = Activity.objects.get(id=id)
    if user.is_staff:
        if request.method == 'POST':
            form = ActivityForm(request.POST,instance=activity)
            if form.is_valid():
                form.save()
                return render_to_response('activity_search.html',
                                          {'user':request.user,
                                           'prompt':True,
                                           'prompt_msg':'活动信息修改成功！',
                                          })
        else:
            form = ActivityForm(instance=activity)
        return render(request, 'modify_activity.html', {
            'form': form,
            'id':id,
            'user':request.user,
        })
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@login_required(login_url='/user_login/')
def delete_activity(request,id):
    user = request.user
    if user.is_staff:
        try:
            activity = Activity.objects.get(id = id)
            activity.delete()
            return render_to_response('activity_search.html',{'user':request.user})
        except Activity.DoesNotExist:
            return render_to_response('activity_search.html',{'user':request.user})
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@csrf_exempt
@login_required(login_url='/user_login/')
def search_activity(request):
    user = request.user
    if user.is_staff:
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
                'user':request.user,
            }
            return render_to_response('activity_search.html',context)
        else:
            activity_list = Activity.objects.all()
            for activity in activity_list:
                activity.start_time = activity.start_time.strftime('%Y-%m-%d')
            context = {
                'activity_list':activity_list,
                'flag':True,
                'user':request.user,
            }
            return render_to_response('activity_search.html',context)
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@csrf_exempt
@login_required(login_url='/user_login/')
def examine_activity(request,id):
    user = request.user
    if user.is_staff:
        if request.method == 'GET':
            activity = Activity.objects.get(id = id)
            activity.start_time = activity.start_time.strftime('%Y-%m-%d')
            studentActivity_list = StudentActivity.objects.filter(activity = activity)
            student_dic = {}
            for studentActivity in studentActivity_list:
                student_dic[studentActivity] = studentActivity.student
            context ={
                'activity': activity,
                'student_dic':student_dic,
                'user':request.user,
            }
            return render_to_response('examine_activity.html',context)
        else:
            activity = Activity.objects.get(id = id)
            studentActivity_list = StudentActivity.objects.filter(activity = activity)
            for studentActivity in studentActivity_list:
                status_str = 'status_'+ str(studentActivity.id)
                award_str = 'award_' + str(studentActivity.id)
                print status_str
                status = request.POST[status_str]
                award = request.POST[award_str]
                studentActivity.status = status
                studentActivity.award = award
                studentActivity.save()
            activity.status = True
            activity.save()
            return redirect(search_activity)
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@login_required(login_url='/user_login/')
def examine_result(request,id):
    user = request.user
    if user.is_staff:
        activity = Activity.objects.get(id = id)
        activity.start_time = activity.start_time.strftime('%Y-%m-%d')
        studentActivity_list = StudentActivity.objects.filter(activity = activity)
        student_dic = {}
        for studentActivity in studentActivity_list:
            student_dic[studentActivity] = studentActivity.student
        context ={
            'activity': activity,
            'student_dic':student_dic,
            'user':request.user,
        }
        return render_to_response('examine_result.html',context)
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@csrf_exempt
@login_required(login_url='/user_login/')
def search_student_activity(request):
    branch_list = PartyBranch.objects.all()
    if request.user.is_staff:
        if request.method == 'POST':
            try:
                branch = request.POST['branch']
                partyBranch = PartyBranch.objects.get(id = branch)
                student_list = Student.objects.filter(party_branch = partyBranch)
                activity_dic = {}
                for student in student_list :
                    activity_count = StudentActivity.objects.filter(student = student).exclude(status=0).count()
                    activity_dic[student] = activity_count
                context = {
                    'flag': True,
                    'activity_dic':activity_dic,
                    'branch_list':branch_list,
                    'user':request.user,
                }
                return render_to_response('student_activity_search.html',context)
            except PartyBranch.DoesNotExist:
                return render_to_response('student_activity_search.html',{'flag':False,'user':request.user})
        else:
            return render_to_response('student_activity_search.html',{'branch_list':branch_list,'user':request.user})
    else:
        return render_to_response('permission_error.html')

@login_required(login_url='/user_login/')
def student_activity_detail(request,id):
    #back
    if request.user.is_staff:
        student = Student.objects.get(id=id)
        studentActivity_list = StudentActivity.objects.filter(student = student)
        activity_dic = {}
        for studentActivity in studentActivity_list:
            activity = studentActivity.activity
            activity.start_time = activity.start_time.strftime('%Y-%m-%d')
            activity_dic[activity] = studentActivity
        context = {
            'activity_dic':activity_dic,
            'student':student,
            'user':request.user,
        }
        return render_to_response('student_activity_detail.html',context)
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@login_required(login_url='/user_login/')
def user_activity_detail(request):
    #student info
    userStudent = UserStudent.objects.get(user=request.user)
    student = userStudent.student
    studentActivity_list = StudentActivity.objects.filter(student = student)
    activity_dic = {}
    for studentActivity in studentActivity_list:
        activity = studentActivity.activity
        activity.start_time = activity.start_time.strftime('%Y-%m-%d')
        activity_dic[activity] = studentActivity
    context = {
        'activity_dic':activity_dic,
        'student':student,
        'user':request.user,
    }
    return render_to_response('student_activity_detail.html',context)

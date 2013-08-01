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
    if 'prompt' in request.GET:
        prompt = request.GET['prompt']
    else:
        prompt = -1
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
    #prompt dic
    prompt_msg = {
        '0':u'取消报名活动成功！',
        '1':u'报名活动成功！',
        '-2':u'超过截止时间,无法报名！',
        '-3':u'活动不存在',
        '-4':u'超过截止时间，无法取消报名',
        '-5':u'未报名此活动！',
    }
    if int(prompt)!=-1:
        context = {
            'activity_list':list,
            'title':title,
            'type':type,
            'user':request.user,
            'prompt':True,
            'prompt_msg': prompt_msg[prompt],
        }
    else:
        context = {
            'activity_list':list,
            'title':title,
            'type':type,
            'user':request.user,
        }
    return render_to_response('activity_list.html',context)

@login_required(login_url='/user_login/')
def join_activity(request,type,id):
    user = request.user
    userStudent = UserStudent.objects.get(user = user)
    student = userStudent.student
    try:
        activity = Activity.objects.get(id=id)
        if activity.deadline >= date.today():
            StudentActivity.objects.get_or_create(student_id = student.id,activity_id = id)
            status = 1
        else:
            print("late for deadline,u can't join it.")
            status = -2
    except Activity.DoesNotExist:
        print('activity does not exist')
        status = -3
    return redirect('/list_activity/%s?prompt=%s'%(type,status))

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
            status = 0
        else:
            status = -4
    except StudentActivity.DoesNotExist:
        status = -5
    return redirect('/list_activity/%s?prompt=%s'%(type,status))

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
                return redirect('/search_activity?operate=1')
        else:
            form = ActivityForm()
        return render(request, 'add_activity.html', {
            'form': form,
            'user':request.user,
        })
    else:
        return render(request,'permission_error.html')

@login_required(login_url='/user_login/')
def modify_activity(request,id):
    user = request.user
    if user.is_staff:
        try:
            activity = Activity.objects.get(id=id)
            if request.method == 'POST':
                form = ActivityForm(request.POST,instance=activity)
                if form.is_valid():
                    form.save()
                    return redirect('/search_activity?operate=2')
            else:
                form = ActivityForm(instance=activity)
            return render(request, 'modify_activity.html', {'form': form,'id':id})
        except Activity.DoesNotExist:
            return redirect('/search_activity?operate=5')
    else:
        return render(request,'permission_error.html')

@login_required(login_url='/user_login/')
def delete_activity(request,id):
    user = request.user
    if user.is_staff:
        try:
            activity = Activity.objects.get(id = id)
            count = StudentActivity.objects.filter(activity=activity).count()
            if count ==0:
                activity.delete()
                return redirect('/search_activity?operate=3')
            else:
                return redirect('/search_activity?operate=6')
        except Activity.DoesNotExist:
            return redirect('/search_activity?operate=5')
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
                list = Activity.objects.filter(type=type,title__contains=title).order_by('-start_time')
            else:
                list = Activity.objects.filter(title__contains=title).order_by('-start_time')
            examine_activity_list = []
            need_examine_activity_list = []
            for activity in list:
                activity.start_time = activity.start_time.strftime('%Y-%m-%d')
                if activity.status:
                    examine_activity_list.append(activity)
                else:
                    need_examine_activity_list.append(activity)
            if len(need_examine_activity_list)==0 and len(examine_activity_list)==0:
                flag = False
            context = {
                'examine_activity_list':examine_activity_list,
                'need_examine_activity_list':need_examine_activity_list,
                'flag':flag,
            }
            return render(request,'activity_search.html',context)
        else:
            activity_list = Activity.objects.all().order_by('-start_time')
            examine_activity_list = []
            need_examine_activity_list = []
            for activity in activity_list:
                activity.start_time = activity.start_time.strftime('%Y-%m-%d')
                if activity.status:
                    examine_activity_list.append(activity)
                else:
                    need_examine_activity_list.append(activity)
            if 'operate' in request.GET:
                operate = request.GET['operate']
                operate_dic = {
                    '1':u'发布活动成功',
                    '2':u'修改活动成功',
                    '3':u'删除活动成功',
                    '4':u'审核活动成功',
                    '5':u'此活动不存在',
                    '6':u'此活动已有人报名，无法删除'
                }
                context = {
                    'prompt':True,
                    'prompt_msg':operate_dic[operate],
                    'need_examine_activity_list':need_examine_activity_list,
                    'examine_activity_list':examine_activity_list,
                    'flag':True,
                }
            else:
                context = {
                    'need_examine_activity_list':need_examine_activity_list,
                    'examine_activity_list':examine_activity_list,
                    'flag':True,
                }
            return render(request,'activity_search.html',context)
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
            return redirect('/search_activity?operate=4')
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

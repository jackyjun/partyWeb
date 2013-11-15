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
                if user.is_active and user.is_superuser==False:
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
                activity.publisher = request.user
                activity.save()
                return redirect('/search_activity?operate=1')
        else:
            form = ActivityForm()
        return render(request, 'add_activity.html', {
            'form': form,
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
def search_single_student_activity(request):
    if request.user.is_staff:
        branch_list = PartyBranch.objects.all()
        if request.method == 'POST':
            student_id = request.POST['student_id']
            name = request.POST['name']
            activity_name = request.POST['activity_name']
            student_list = Student.objects.filter(student_id__contains=student_id,name__contains=name)
            activity_list = Activity.objects.filter(title__contains=activity_name)
            dic = {}
            for activity in activity_list:
                student_activity_list = StudentActivity.objects.filter(activity=activity)
                student_activity_dic = {}
                for student_activity in student_activity_list:
                    for student in student_list:
                        if student_activity.student == student:
                            student_activity_dic[student] = student_activity
                if len(student_activity_dic):
                    dic[activity] = student_activity_dic
            print dic
            context = {
                'dic':dic,
                'branch_list':branch_list,
                'flag':True,
                'table_type':2,
            }
            return render(request,'student_activity_search.html',context)
        else:
            return render(request,'student_activity_search.html',{'branch_list':branch_list})
    else:
        return render(request,'permission_error.html')

@csrf_exempt
@login_required(login_url='/user_login/')
def search_student_activity(request):
    #search multiply student activity
    branch_list = PartyBranch.objects.all()
    if request.user.is_staff:
        if request.method == 'POST':
            try:
                branch = request.POST['branch']
                student_id = request.POST['student_id']
                name = request.POST['name']
                start_time_str = request.POST['start_time']
                end_time_str = request.POST['end_time']
                if start_time_str == '':
                    start_time_str = '1970-1-1'
                if end_time_str =='':
                    end_time_str = '2050-1-1'
                if request.POST['type']!='-1':
                    type = [int(request.POST['type'])]
                else:
                    type = [0,1,2,3]
                start_time = datetime.strptime(start_time_str,'%Y-%m-%d')
                end_time = datetime.strptime(end_time_str,'%Y-%m-%d')
                if branch == '-1':
                    student_list = Student.objects.filter(student_id__contains=student_id,name__contains=name)
                else:
                    student_list = Student.objects.filter(student_id__contains=student_id,name__contains=name,party_branch_id = branch)
                activity_dic = {}
                for student in student_list :
                    student_activity_list = StudentActivity.objects.filter(student = student).exclude(status=0)
                    activity_count = 0
                    for student_activity in student_activity_list:
                        activity = Activity.objects.get(id = student_activity.activity_id)
                        if activity.type in type:
                            activity_start_time = datetime.combine(activity.start_time,time())
                            if activity_start_time>=start_time and activity_start_time<=end_time:
                                activity_count += 1
                    activity_dic[student] = activity_count
                context = {
                    'flag': True,
                    'table_type':1,
                    'activity_dic':activity_dic,
                    'branch_list':branch_list,
                    'user':request.user,
                    'start_time':start_time_str,
                    'end_time':end_time_str,
                    'type':request.POST['type'],
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
        type = request.GET['type']
        start_time = request.GET['start_time']
        end_time = request.GET['end_time']
        if start_time == '':
            start_time = '1970-1-1'
        if end_time =='':
            end_time = '2050-1-1'
        if request.GET['type']=='-1':
            type = [0,1,2,3]
        else:
            type = [int(request.GET['type'])]
        start_time = datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.strptime(end_time,'%Y-%m-%d')
        student = Student.objects.get(id=id)
        studentActivity_list = StudentActivity.objects.filter(student = student)
        activity_dic = {}
        for studentActivity in studentActivity_list:
            activity = studentActivity.activity
            activity_start_time = datetime.combine(activity.start_time,time())
            if activity_start_time>=start_time and activity_start_time<=end_time and activity.type in type:
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
    activity_summary_dic = {}
    activity_num = 0
    graduates_activity_num = 0
    youth_activity_num = 0
    other_activity_num = 0
    party_activity_num = 0
    for studentActivity in studentActivity_list:
        activity = studentActivity.activity
        activity.start_time = activity.start_time.strftime('%Y-%m-%d')
        activity_dic[activity] = studentActivity
        if studentActivity.status !=0:
            type = activity.type
            if type == 0:
                graduates_activity_num += 1
            elif type == 1:
                youth_activity_num += 1
            elif type == 2:
                other_activity_num += 1
            elif type == 3:
                party_activity_num += 1
            activity_num += 1
    context = {
        'activity_num' : activity_num,
        'graduates_activity_num' : graduates_activity_num,
        'youth_activity_num': youth_activity_num,
        'other_activity_num': other_activity_num,
        'party_activity_num': party_activity_num,
        'activity_dic':activity_dic,
        'activity_summary_dic':activity_summary_dic,
        'student':student,
        'user':request.user,
    }
    return render_to_response('user_activity_detail.html',context)

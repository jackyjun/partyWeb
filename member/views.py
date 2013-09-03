#coding=utf-8
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from models import Student,StudentForm,StudentAssessment,PartyBranch,UserStudent
from documents.models import News,Notice,NivoSlider
from activity.models import Activity
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import *

@csrf_exempt
def user_login(request):
#home page login
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            #s = Student(user_id = user.id,party_branch_id=1)
            #s.save()
            #return redirect(home)
            dic = {'username': user.username,'id':user.id,'status':1}
        else:
           dic = {'status': 0,'errorMsg':u'登录错误！'}
    else:
        # Return an 'invalid login' error message.
       dic = {'status': 0,'errorMsg':u'用户名或密码错误！'}
    return HttpResponse(json.dumps(dic))

@csrf_exempt
def login_view(request):
#login page
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                student = Student.objects.get_or_create(student_id=user.username)
                UserStudent.objects.get_or_create(student=student[0],user=user)
                return redirect('/student_center/')
            else:
                return render(request,'login.html',{'errorMsg':'登录错误'})
        else:
            # Return an 'invalid login' error message.
            return render(request,'login.html',{'errorMsg':'用户名或密码错误'})
    else:
        return render(request,'login.html')

def user_logout(request):
      logout(request)
      return redirect(home)

@login_required(login_url='/user_login/')
def student_info(request):
    user = request.user
    if request.method == 'POST':
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        form = StudentForm(request.POST,instance=student) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            student = form.save(commit=False)
            if student.party_branch_id:
                student.save()
            else:
                student.party_branch_id = 1
                student.save()
            return redirect('/student_info?update=True')
        else:
            userStudent = UserStudent.objects.get(user = user)
            student = userStudent.student
            student_dic = {}
            student_dic[u'政治面貌'] = student.get_political_status_display
            if student.league_member:
                student_dic[u'是否团员'] = u'是'
            else:
                student_dic[u'是否团员'] = u'否'
            student_dic[u'申请加入共产党时间'] = student.apply_party_time.strftime('%Y-%m-%d')
            student_dic[u'加入共产党时间'] =   student.join_party_time.strftime('%Y-%m-%d')
            student_dic[u'所属党支部'] = student.party_branch
            context = {
                'form': form,
            }
            return render(request, 'student_info.html',context)
    else:
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        student_dic = {}
        student_dic[u'政治面貌'] = student.get_political_status_display
        if student.league_member:
            student_dic[u'是否团员'] = u'是'
        else:
            student_dic[u'是否团员'] = u'否'
        student_dic[u'申请加入共产党时间'] = student.apply_party_time.strftime('%Y-%m-%d')
        student_dic[u'加入共产党时间'] =   student.join_party_time.strftime('%Y-%m-%d')
        student_dic[u'所属党支部'] = student.party_branch
        form = StudentForm(instance=student)
        if 'update'in request.GET:
            context = {
                'prompt':True,
                'prompt_msg':'修改成功',
                'form': form,
                'student':student_dic,
            }
        else:
            context = {
                'form': form,
                'student':student_dic,
            }
        return render(request, 'student_info.html', context)

@login_required(login_url='/user_login/')
def student_center(request):
    student = UserStudent.objects.get(user = request.user).student
    return render(request,'student_center.html',{'student':student})

@login_required(login_url='/user_login/')
def admin_center(request):
    student = UserStudent.objects.get(user = request.user).student
    if request.user.is_staff:
        return render(request,'admin_center.html',{'student':student})
    else:
        return render(request,'permission_error.html')
@login_required(login_url='/user_login/')
def back_student_info(request,id):
    user = request.user
    if user.is_staff:
        student = Student.objects.get(id=id)
        form = StudentForm(instance=student)
        return render(request, 'back_student_info.html', {
            'form': form,
            'student':student,
            'user':request.user,
        })
    else:
        return render_to_response('permission_error.html')

def branch_summary(request):
    branch_list = PartyBranch.objects.all()
    context = {}
    for branch in branch_list:
        student_list = Student.objects.filter(party_branch_id = branch.id)
        masses_list = student_list.filter(political_status=0)
        activist_list = student_list.filter(political_status=1)
        probationary_list = student_list.filter(political_status=2)
        official_list = student_list.filter(political_status=3)
        dic = {
            'masses': len(masses_list),
            'activist':len(activist_list),
            'probationary':len(probationary_list),
            'official':len(official_list),
        }
        list = [len(official_list),len(probationary_list),len(activist_list)]
        context[branch] = list
    return render_to_response('branch_summary.html',{'context':context,'user':request.user})

def branch_detail(request,id):
    branch = PartyBranch.objects.get(id = id)
    student_list = Student.objects.filter(party_branch_id = id)
    masses_list = student_list.filter(political_status=0)
    activist_list = student_list.filter(political_status=1)
    probationary_list = student_list.filter(political_status=2)
    official_list = student_list.filter(political_status=3)
    context = {
        'branch':branch,
        'masses_list': masses_list,
        'activist_list':activist_list,
        'probationary_list':probationary_list,
        'official_list':official_list,
        'user':request.user,
    }
    return render_to_response('branch_detail.html',context)

@login_required(login_url='/user_login/')
def branch_assessment(request):
    user = request.user
    userStudent = UserStudent.objects.get(user = user)
    student = userStudent.student
    branch = PartyBranch.objects.get(id = student.party_branch_id)
    student_list = Student.objects.filter(party_branch_id = student.party_branch_id)
    assessment_dic = {}
    for student in student_list:
        list = StudentAssessment.objects.filter(student = student)
        assessment_dic[student] = list
    context = {
        'branch':branch,
        'assessment_dic':assessment_dic,
        'user':request.user,
    }
    return render_to_response('branch_assessment.html',context)

def home(request):
    NEWS_NUMBER = 8
    Notice_NUMBER = 8
    ACTIVITY_NUMBER = 3
    NIVOSLIDER_NUMBER = 4
    news = News.objects.all().order_by('-date')[:NEWS_NUMBER]
    notices = Notice.objects.all().order_by('-date')[:Notice_NUMBER]
    nivosliders = NivoSlider.objects.all()
    graduates_activity = Activity.objects.filter(type=0).order_by('-start_time')[:ACTIVITY_NUMBER]
    youth_activity = Activity.objects.filter(type=1).order_by('-start_time')[:ACTIVITY_NUMBER]
    party_activity = Activity.objects.filter(type=2).order_by('-start_time')[:ACTIVITY_NUMBER]
    other_activity = Activity.objects.filter(type=3).order_by('-start_time')[:ACTIVITY_NUMBER]
    for item in news:
        item.date = item.date.strftime('%Y-%m-%d')
    for item in notices:
        item.date = item.date.strftime('%Y-%m-%d')
    for item in graduates_activity:
        item.start_time = item.start_time.strftime('%Y-%m-%d')
    for item in youth_activity:
        item.start_time = item.start_time.strftime('%Y-%m-%d')
    for item in party_activity:
        item.start_time = item.start_time.strftime('%Y-%m-%d')
    for item in other_activity:
        item.start_time = item.start_time.strftime('%Y-%m-%d')
    branch_list = PartyBranch.objects.all()[:5]
    context = {
        'news':news,
        'notices':notices,
        'nivosliders':nivosliders,
        'branch_list':branch_list,
        'graduates_activity':graduates_activity,
        'youth_activity':youth_activity,
        'party_activity':party_activity,
        'other_activity':other_activity,
    }
    return render_to_response('home3.html',context,context_instance=RequestContext(request))

@csrf_exempt
def branch_search(request):
    branch_list = PartyBranch.objects.all()
    if request.method == 'POST':
        branch = request.POST['branch']
        status = request.POST['status']
        if int(branch):
            student_list = Student.objects.filter(party_branch_id = branch,political_status = status)
        else:
            student_list = Student.objects.filter(political_status = status)
        for student in student_list:
            if student.apply_party_time or student.join_party_time:
                student.apply_party_time = student.apply_party_time.strftime('%Y-%m-%d')
                student.join_party_time = student.join_party_time.strftime('%Y-%m-%d')
        if len(student_list)==0:
            status = u'0'
        context = {
            'student_list':student_list,
            'branch_list':branch_list,
            'type': status,
            'user':request.user,
        }
        print student_list
        return render_to_response('branch_search.html',context)
    else:
        return render_to_response('branch_search.html',{'branch_list':branch_list,'user':request.user})

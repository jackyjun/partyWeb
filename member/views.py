#coding=utf-8
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from models import Student,StudentForm,StudentAssessment
from documents.models import News,Notice
from activity.models import Activity
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def user_login(request):
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

def user_logout(request):
      logout(request)
      return redirect(home)

def student_info(request):
    if request.method == 'POST':
        user = request.user
        student = Student.objects.get(id=1)
        form = StudentForm(request.POST,instance=student) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return render_to_response('error.html',{'msg':'username error'})
    else:
        a = Student.objects.get(id=1)
        form = StudentForm(instance=a)
        #form = NewsForm() # An unbound form

    return render(request, 'home.html', {
        'form': form,
    })

def branch_detail(request,id):
    student_list = Student.objects.filter(party_branch_id = id)
    masses_list = student_list.filter(political_status=0)
    activist_list = student_list.filter(political_status=1)
    probationary_list = student_list.filter(political_status=2)
    official_list = student_list.filter(political_status=3)
    context = {
        'masses_list': masses_list,
        'activist_list':activist_list,
        'probationary_list':probationary_list,
        'official_list':official_list,
    }
    return render_to_response('branch_detail.html',context)

def branch_assessment(request,id):
    student_list = Student.objects.filter(party_branch_id = id)
    assessment_dic = {}
    for student in student_list:
        list = StudentAssessment.objects.filter(student = student)
        assessment_dic[student] = list
    print  assessment_dic
    return render_to_response('branch_assessment.html',{'assessment_dic':assessment_dic})

def home(request):
    user = request.user
    NEWS_NUMBER = 10
    Notice_NUMBER = 7
    ACTIVITY_NUMBER = 3
    news = News.objects.all().order_by('-date')[:NEWS_NUMBER]
    notices = Notice.objects.all().order_by('-date')[:Notice_NUMBER]
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
    context = {
        'user':user,
        'news':news,
        'notices':notices,
        'graduates_activity':graduates_activity,
        'youth_activity':youth_activity,
        'party_activity':party_activity,
        'other_activity':other_activity,
    }
    return render_to_response('home.html',context,context_instance=RequestContext(request))

def student_list_search(request,branch,status):
    if int(branch):
        student_list = Student.objects.filter(party_branch_id = branch,political_status = status)
    else:
        student_list = Student.objects.all()
    return render_to_response('search_list.html',{'student_list':student_list})

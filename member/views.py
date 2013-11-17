#coding=utf-8
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from models import Student,StudentForm,StudentAssessment,PartyBranch,UserStudent,ImportXlsForm
from documents.models import News,Notice,NivoSlider
from activity.models import Activity
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
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
                if user.is_staff:
                    return redirect('/admin_center/')
                else:
                    return redirect('/student_center/')
            else:
                return render(request,'login.html',{'errorMsg':'登录错误'})
        else:
            # Return an 'invalid login' error message.
            return render(request,'login.html',{'errorMsg':'用户名或密码错误'})
    else:
        return render(request,'login.html')

@csrf_exempt
@login_required(login_url='/user_login/')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = authenticate(username=request.user.username,password=old_password)
        if user is not None:
            if user.is_active:
                user.set_password(new_password)
                user.save()
                return render(request,'change_password.html',{'prompt':True,'prompt_msg':'修改密码成功'})
            else:
                 return render(request,'change_password.html',{'prompt':True,'prompt_msg':'修改密码失败'})
        else:
            return render(request,'change_password.html',{'prompt':True,'prompt_msg':'原密码错误'})
    else:
        return render(request,'change_password.html')

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
            student_list = []
            student_dic = {}
            student_dic[u'学科类型'] = student.get_subject_display()
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'培养类型'] = student.get_training_display()
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'专业'] = student.major
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'性别'] = student.get_gender_display()
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'实验室'] = student.laboratory
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'座位号'] = student.seat_number
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'职位'] = student.duty
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'政治面貌'] = student.get_political_status_display
            student_list.append(student_dic)
            student_dic = {}
            if student.apply_party_time:
                student.apply_party_time = student.apply_party_time.strftime('%Y-%m-%d')
            student_dic[u'入党时间'] = student.apply_party_time
            student_list.append(student_dic)
            student_dic = {}
            if student.join_party_time:
                student.join_party_time = student.join_party_time.strftime('%Y-%m-%d')
            student_dic[u'转正时间'] =   student.join_party_time
            student_list.append(student_dic)
            student_dic = {}
            student_dic[u'所属党支部'] = student.party_branch
            student_list.append(student_dic)
            context = {
                'form': form,
                'student_list':student_list,
            }
            return render(request, 'student_info.html',context)
    else:
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        student_list = []
        student_dic = {}
        student_dic[u'学科类型'] = student.get_subject_display()
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'培养类型'] = student.get_training_display()
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'专业'] = student.major
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'性别'] = student.get_gender_display()
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'实验室'] = student.laboratory
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'座位号'] = student.seat_number
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'职位'] = student.duty
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'政治面貌'] = student.get_political_status_display
        student_list.append(student_dic)
        student_dic = {}
        if student.apply_party_time:
            student.apply_party_time = student.apply_party_time.strftime('%Y-%m-%d')
        student_dic[u'入党时间'] = student.apply_party_time
        student_list.append(student_dic)
        student_dic = {}
        if student.join_party_time:
            student.join_party_time = student.join_party_time.strftime('%Y-%m-%d')
        student_dic[u'转正时间'] =   student.join_party_time
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'所属党支部'] = student.party_branch
        student_list.append(student_dic)
        form = StudentForm(instance=student)
        if 'update'in request.GET:
            context = {
                'prompt':True,
                'prompt_msg':'修改成功',
                'form': form,
                'student':student,
                'student_list':student_list,
            }
        else:
            context = {
                'form': form,
                'student':student,
                'student_list':student_list,
            }
        return render(request, 'student_info.html', context)

@login_required(login_url='/user_login/')
def student_center(request):
    #student = UserStudent.objects.get(user = request.user).student
    #return render(request,'student_center.html',{'student':student})
    return redirect("/student_info/")

@login_required(login_url='/user_login/')
def admin_center(request):
    if request.user.is_superuser:
         return redirect("/search_activity/")
    else:
        student = UserStudent.objects.get(user = request.user).student
        if request.user.is_staff:
             return redirect("/search_activity/")
        else:
            return render(request,'permission_error.html')

@login_required(login_url='/user_login/')
def back_student_info(request,id):
    user = request.user
    if user.is_staff:
        student = Student.objects.get(id=id)
        student_list = []
        student_dic = {}
        student_dic[u'学号'] = student.student_id
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'姓名'] = student.name
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'学科类型'] = student.get_subject_display()
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'培养类型'] = student.get_training_display()
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'专业'] = student.major
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'导师'] = student.professor
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'性别'] = student.get_gender_display()
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'寝室号'] = student.dormitory
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'实验室'] = student.laboratory
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'座位号'] = student.seat_number
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'职位'] = student.duty
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'政治面貌'] = student.get_political_status_display
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'入党时间'] = student.apply_party_time
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'转正时间'] =   student.join_party_time
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'所属党支部'] = student.party_branch
        student_list.append(student_dic)
        student_dic = {}
        student_dic[u'手机号码'] = student.phone
        student_list.append(student_dic)
        student_dic = {}
        student_list.append(student_dic)
        return render(request, 'back_student_info.html', {
            'student_list':student_list,
            'user':request.user,
        })
    else:
        return render_to_response('permission_error.html')

@csrf_exempt
def student_search(request):
    user = request.user
    student_list = []
    if user.is_staff:
        party_branch_list = PartyBranch.objects.all()
        context = {}
        context['party_branch_list'] = party_branch_list
        if request.method=='GET':
            return render(request,'student_search.html',context)
        else:
            student_id = request.POST['student_id']
            name = request.POST['name']
            if request.POST['subject']!='-1':
                subject = [int(request.POST['subject'])]
            else:
                subject = [0,1,2,3]
            if request.POST['training']!='-1':
                training = [int(request.POST['training'])]
            else:
                training = [0,1]
            if request.POST['gender']!='-1':
                gender = [int(request.POST['gender'])]
            else:
                gender = [0,1]
            if request.POST['political_status']!='-1':
                political_status = [int(request.POST['political_status'])]
            else:
                political_status = [0,1,2,3]
            major = request.POST['major']
            professor = request.POST['professor']
            phone = request.POST['phone']
            dormitory = request.POST['dormitory']
            laboratory = request.POST['laboratory']
            seat_number = request.POST['seat_number']
            if request.POST['party_branch_id']!='-1':
                student_list = Student.objects.filter(
                                        student_id__contains=student_id,
                                        name__contains=name,
                                        subject__in=subject,
                                        training__in=training,
                                        gender__in = gender,
                                        major__contains=major,
                                        professor__contains=professor,
                                        phone__contains=phone,
                                        dormitory__contains=dormitory,
                                        laboratory__contains=laboratory,
                                        seat_number__contains=seat_number,
                                        party_branch_id=request.POST['party_branch_id'],
                                        political_status__in=political_status
                                    )
            else:
                student_list = Student.objects.filter(
                                                        student_id__contains=student_id,
                                                        name__contains=name,
                                                        subject__in=subject,
                                                        training__in=training,
                                                        gender__in = gender,
                                                        major__contains=major,
                                                        professor__contains=professor,
                                                        phone__contains=phone,
                                                        dormitory__contains=dormitory,
                                                        laboratory__contains=laboratory,
                                                        seat_number__contains=seat_number,
                                                        political_status__in=political_status
                                                    )
            context['student_list'] = student_list
            print student_list
            return render(request,'student_search.html',context)
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
    for item in student_list:
        if item.apply_party_time:
            item.apply_party_time = item.apply_party_time.strftime('%Y-%m-%d')
        if item.join_party_time:
            item.join_party_time = item.join_party_time.strftime('%Y-%m-%d')
    for item in masses_list:
        if item.apply_party_time:
            item.apply_party_time = item.apply_party_time.strftime('%Y-%m-%d')
        if item.join_party_time:
            item.join_party_time = item.join_party_time.strftime('%Y-%m-%d')
    for item in activist_list:
        if item.apply_party_time:
            item.apply_party_time = item.apply_party_time.strftime('%Y-%m-%d')
        if item.join_party_time:
            item.join_party_time = item.join_party_time.strftime('%Y-%m-%d')
    for item in probationary_list:
        if item.apply_party_time:
            item.apply_party_time = item.apply_party_time.strftime('%Y-%m-%d')
        if item.join_party_time:
            item.join_party_time = item.join_party_time.strftime('%Y-%m-%d')
    for item in official_list:
        if item.apply_party_time:
            item.apply_party_time = item.apply_party_time.strftime('%Y-%m-%d')
        if item.join_party_time:
            item.join_party_time = item.join_party_time.strftime('%Y-%m-%d')
    context = {
        'branch':branch,
        'masses_list': masses_list,
        'activist_list':activist_list,
        'probationary_list':probationary_list,
        'official_list':official_list,
        'masses_count':len(masses_list),
        'activist_count':len(activist_list),
        'probationary_count':len(probationary_list),
        'official_count':len(official_list),
    }
    return render(request,'branch_detail.html',context)

@login_required(login_url='/user_login/')
def branch_assessment(request):
    user = request.user
    if user.is_superuser:
        context = {
        }
        pass
    else:
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
        }
    return render(request,'branch_assessment.html',context)

def branch_structure(request):
    return render(request,'branch_structure.html')

def old_home(request):
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
    return render(request,'home4.html',context)

def home(request):
    NEWS_NUMBER = 5
    Notice_NUMBER = 5
    ACTIVITY_NUMBER = 7
    NIVOSLIDER_NUMBER = 4
    news = News.objects.all().order_by('-date')[:NEWS_NUMBER]
    notices = Notice.objects.filter(type=1).order_by('-date')[:Notice_NUMBER]
    develop_notices = Notice.objects.all().order_by('-date').filter(type=2)[:Notice_NUMBER]
    nivosliders = NivoSlider.objects.all()
    graduates_activity = Activity.objects.filter(type=0).order_by('-start_time')[:ACTIVITY_NUMBER]
    youth_activity = Activity.objects.filter(type=1).order_by('-start_time')[:ACTIVITY_NUMBER]
    party_activity = Activity.objects.filter(type=2).order_by('-start_time')[:ACTIVITY_NUMBER]
    other_activity = Activity.objects.filter(type=3).order_by('-start_time')[:ACTIVITY_NUMBER]
    for item in news:
        item.date = item.date.strftime('%Y-%m-%d')
    for item in notices:
        item.date = item.date.strftime('%Y-%m-%d')
    for item in develop_notices:
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
    branch_context = {}
    for branch in branch_list:
        student_list = Student.objects.filter(party_branch_id = branch.id)
        masses_list = student_list.filter(political_status=0)
        activist_list = student_list.filter(political_status=1)
        probationary_list = student_list.filter(political_status=2)
        official_list = student_list.filter(political_status=3)
        list = [len(official_list),len(probationary_list),len(activist_list)]
        branch_context[branch] = list
    context = {
        'branch_context':branch_context,
        'news':news,
        'notices':notices,
        'develop_notices':develop_notices,
        'nivosliders':nivosliders,
        'graduates_activity':graduates_activity,
        'youth_activity':youth_activity,
        'party_activity':party_activity,
        'other_activity':other_activity,
    }
    return render(request,'home5.html',context)

def contact(request):
    return render(request,'contact.html')

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
            if student.apply_party_time:
                student.apply_party_time = student.apply_party_time.strftime('%Y-%m-%d')
            if student.join_party_time:
                student.join_party_time = student.join_party_time.strftime('%Y-%m-%d')
        if len(student_list)==0:
            status = u'0'
        context = {
            'student_list':student_list,
            'branch_list':branch_list,
            'type': status,
            'user':request.user,
        }
        return render_to_response('branch_search.html',context)
    else:
        return render_to_response('branch_search.html',{'branch_list':branch_list,'user':request.user})

@csrf_exempt
@login_required(login_url='/user_login/')
def import_xls(request):
    #import student info
    FILE_PATH = '/home/sjh/test.xls'
    from xlrd import open_workbook
    import re
    if request.user.is_staff:
        if request.method == 'POST':
            form = ImportXlsForm(request.POST, request.FILES)
            if form.is_valid():
                f = request.FILES['file']
                if re.match(r'\w+\.xls',f.name):
                    print f.name
                    with open(FILE_PATH, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    GENDER_CHOICE = {
                        0: u'男',
                        1: u'女',
                    }
                    POLITICAL_STATUS_CHOICE = {
                        0: u'群众',
                        1: u'共青团员',
                        2: u'预备党员',
                        3: u'正式党员',
                    }
                    SUBJECT_CHOICE = {
                        0:u'学术型硕士',
                        1:u'专业型硕士',
                        2:u'联合培养型硕士',
                        3:u'博士',
                    }
                    TRAINING_CHOICE = {
                        0:u'统分',
                        1:u'委培',
                    }
                    wb = open_workbook(FILE_PATH)
                    s = wb.sheets()[0]
                    test_time = date.today()
                    for row in range(1,s.nrows):
                        #load data by row
                        values = []
                        for col in range(s.ncols):
                            #load data by col
                            values.append(s.cell(row,col).value)

                        #subject_choice
                        subject = 0
                        for k,v in SUBJECT_CHOICE.items():
                            if values[2] == v:
                                subject = k
                                break

                        #training_choice
                        training = 0
                        for k,v in TRAINING_CHOICE.items():
                            if values[3] == v:
                                training = k
                                break

                        #gender_choice
                        gender = 0
                        for k,v in GENDER_CHOICE.items():
                            if values[6] == v:
                                gender = k
                                break

                        #political_status
                        political_status = 0
                        for k,v in POLITICAL_STATUS_CHOICE.items():
                            if values[12] == v:
                                political_status = k
                                break

                        #party_branch
                        party_branch_id = 1
                        party_branch_list = PartyBranch.objects.all()
                        for party_branch in party_branch_list:
                            if values[11] == party_branch.name:
                                party_branch_id = party_branch.id
                                break

                        #party_time
                        apply_party_time = None
                        join_party_time = None
                        if re.match(r'\d{4}-\d{1,2}-\d{1,2}',str(values[13])):
                            apply_party_time = datetime.strptime(str(values[13]),'%Y-%m-%d').date()
                        if re.match(r'\d{4}-\d{1,2}-\d{1,2}',str(values[14])):
                            join_party_time = datetime.strptime(str(values[14]),'%Y-%m-%d').date()
                        user = User.objects.create_user(str(long(values[0])),None,str(long(values[0])))
                        user.first_name = values[1]
                        user.save()
                        student = Student.objects.get_or_create(
                                    student_id=str(long(values[0])),
                                    name = values[1],
                                    subject = subject,
                                    training = training,
                                    major = values[4],
                                    professor = values[5],
                                    gender = gender,
                                    phone = str(long(values[7])),
                                    dormitory = values[8],
                                    laboratory = str(long(values[9])),
                                    seat_number = str(long(values[10])),
                                    party_branch_id = party_branch_id,
                                    political_status = political_status,
                                    apply_party_time = apply_party_time,
                                    join_party_time = join_party_time,
                                    duty = values[15]
                                )
                        UserStudent.objects.get_or_create(user=user,student=student[0])
                    context = {
                        'form':form,
                        'prompt':True,
                        'prompt_msg':'数据读入成功！'
                    }
                    return render(request,'import_xls.html',context)
                else:
                    context = {
                        'form':form,
                        'prompt':True,
                        'prompt_msg':'上传文件格式不对，请重新上传'
                    }
                    return render(request,'import_xls.html',context)
        else:
            form = ImportXlsForm()
            return render(request,'import_xls.html', {'form': form})
    else:
        return render(request,'permission_error.html')

def version(request):
    return render(request,'version.html')
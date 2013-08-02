# Create your views here.
#coding=utf-8
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render,redirect
from django.views.decorators.csrf import csrf_exempt
from member.models import UserStudent,Student
from models import News,Regulation,Notice,Price,StudentPrice,Attachment,AttachmentForm
from django.contrib.auth.decorators import login_required
from datetime import *
from django.http import HttpResponse

def get_news(request,id):
    try:
        news = News.objects.get(id=id)
        news.date = news.date.strftime('%Y-%m-%d')
        return render_to_response('news.html',{'news':news,'user':request.user})
    except News.DoesNotExist:
        return render_to_response('error.html',{'msg':'news does not exist.'})

def get_notice(request,id):
    try:
        notice = Notice.objects.get(id=id)
        notice.date = notice.date.strftime('%Y-%m-%d')
        return render_to_response('detail.html',{'detail':notice,'user':request.user})
    except Notice.DoesNotExist:
        return render_to_response('error.html',{'msg':'notice does not exist.'})

def get_regulation(request,id):
    try:
        regulation = Regulation.objects.get(id=id)
        regulation.date = regulation.date.strftime('%Y-%m-%d')
        return render_to_response('detail.html',{'detail':regulation,'user':request.user})
    except Regulation.DoesNotExist:
        return render_to_response('error.html',{'msg':'regulation does not exist.'})

def list_news(request,page):
    NEWS_COUNT = 10
    item_list = News.objects.all().order_by('-date').order_by('-id')
    paginator = Paginator(item_list,NEWS_COUNT)
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_list = paginator.page(paginator.num_pages)
    for news in news_list:
        news.date = news.date.strftime('%Y-%m-%d')
    return render_to_response('list.html',{'item_list':news_list,'title':u'新闻动态','type':'news','user':request.user})

def list_notice(request,type,page):
    #type 0 == all
    title = u'通知公告'
    choice = Notice.TYPE_CHOICE
    NOTICE_COUNT = 10
    if int(type):
        title = choice[int(type)-1][1]
        item_list = Notice.objects.filter(type=type).order_by('-date').order_by('-id')
    else:
        item_list = Notice.objects.all().order_by('-date').order_by('-id')
    paginator = Paginator(item_list,NOTICE_COUNT)
    try:
        notice_list = paginator.page(page)
    except PageNotAnInteger:
        notice_list = paginator.page(1)
    except EmptyPage:
        notice_list = paginator.page(paginator.num_pages)
    for notice in notice_list:
        notice.date = notice.date.strftime('%Y-%m-%d')
    return render_to_response('list.html',{'item_list':notice_list,'title':title,'type':'notice','user':request.user})

def list_regulation(request,page):
    REGULATION_COUNT = 10
    item_list = Regulation.objects.all().order_by('-date')
    paginator = Paginator(item_list,REGULATION_COUNT)
    try:
        regulation_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        regulation_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        regulation_list = paginator.page(paginator.num_pages)
    for regulation in regulation_list:
        regulation.date = regulation.date.strftime('%Y-%m-%d')
    return render_to_response('list.html',
                              {
                                'item_list':regulation_list,
                               'title':u'制度条例',
                               'type':'regulation',
                               'user':request.user
                              })

def list_price(request):
    price_list = Price.objects.all().order_by('-deadline')
    list = []
    for price in price_list:
        price_dic = {}
        if price.deadline >= date.today():
            try:
                if request.user.is_active:
                    userStudent = UserStudent.objects.get(user = request.user)
                    student = userStudent.student
                    StudentPrice.objects.get(student_id = student.id,price_id = price.id)
                    flag = 1
                else:
                    flag = 0
            except StudentPrice.DoesNotExist:
                flag = 0
            price.date = price.date.strftime('%Y-%m-%d')
            price.deadline = price.deadline.strftime('%Y-%m-%d')
            price_dic[price] = flag
            list.append(price_dic)
    prompt_msg = {
        '1':u'申请奖项成功！',
        '2':u'取消申请奖项成功！',
        '-1':u'超过截止时间,无法申请！',
        '-2':u'奖项不存在',
        '-3':u'超过截止时间，无法取消申请',
        '-4':u'未申请此奖项！',
    }
    if 'status' in request.GET:
        prompt = request.GET['status']
    else:
        prompt = 0
    if int(prompt)!=0:
        context = {
            'price_list':list,
            'prompt':True,
            'prompt_msg': prompt_msg[prompt],
        }
    else:
        context = {
            'price_list':list,
        }
    return render(request,'price_list.html',context)

def price_detail(request,id):
    try:
        price = Price.objects.get(id=id)
        price.date = price.date.strftime('%Y-%m-%d')
        return render_to_response('price_detail.html',{'price':price,'user':request.user})
    except Price.DoesNotExist:
        return redirect(list_price)

@login_required(login_url='/user_login/')
def apply_price(request,id):
    user = request.user
    userStudent = UserStudent.objects.get(user = user)
    student = userStudent.student
    try:
        price = Price.objects.get(id=id)
        if price.deadline >= date.today():
            StudentPrice.objects.get_or_create(student_id = student.id,price_id = id)
            status = 1
        else:
            status = -1
    except Price.DoesNotExist:
        status = -2
    return redirect('/list_price?status=%s'%status)

@login_required(login_url='/user_login/')
def cancel_price(request,id):
    user = request.user
    userStudent = UserStudent.objects.get(user = user)
    student = userStudent.student
    try:
        price = Price.objects.get(id=id)
        if price.deadline >date.today():
            studentPrice= StudentPrice.objects.get(student_id = student.id,price_id = id)
            studentPrice.delete()
            status = 2
        else:
            status = -3
    except StudentPrice.DoesNotExist:
        status = -4
    return redirect('/list_price?status=%s'%status)

@login_required(login_url='/user_login/')
def student_price(request):
    #student center
    student = UserStudent.objects.get(user=request.user).student
    studentPrice_list = StudentPrice.objects.filter(student = student)
    price_dic = {}
    for studentPrice in studentPrice_list:
        price = studentPrice.price
        price.date = price.date.strftime('%Y-%m-%d')
        price.deadline = price.deadline.strftime('%Y-%m-%d')
        price_dic[studentPrice] = price
    print price_dic
    return render_to_response('student_price.html',{'price_dic':price_dic,'user':request.user})

@csrf_exempt
@login_required(login_url='/user_login/')
def examine_price(request,id):
    user = request.user
    if user.is_superuser:
        if request.method == 'GET':
            price = Price.objects.get(id = id)
            price.date = price.date.strftime('%Y-%m-%d')
            studentPrice_list = StudentPrice.objects.filter(price = price)
            student_dic = {}
            for studentPrice in studentPrice_list:
                student_dic[studentPrice] = studentPrice.student
            context ={
                'price': price,
                'student_dic':student_dic,
                'user':request.user,
            }
            return render_to_response('examine_price.html',context)
        else:
            price = Price.objects.get(id = id)
            studentPrice_list = StudentPrice.objects.filter(price = price)
            for studentPrice in studentPrice_list:
                status_str = 'status_'+ str(studentPrice.id)
                print status_str
                status = request.POST[status_str]
                studentPrice.status = status
                studentPrice.save()
                price.status = True
                price.save()
            return redirect('/examine_price_list/?examine=True')
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@login_required(login_url='/user_login/')
def examine_price_result(request,id):
    user = request.user
    if user.is_superuser:
        price = Price.objects.get(id = id)
        price.date = price.date.strftime('%Y-%m-%d')
        studentPrice_list = StudentPrice.objects.filter(price = price)
        student_dic = {}
        for studentPrice in studentPrice_list:
            student_dic[studentPrice] = studentPrice.student
        context ={
            'price': price,
            'student_dic':student_dic,
            'user':request.user,
        }
        return render_to_response('examine_price_result.html',context)
    else:
        return render_to_response('permission_error.html',{'user':request.user})

@login_required(login_url='/user_login/')
def examine_price_list(request):
    if request.user.is_superuser:
        price_list = Price.objects.all()
        for price in price_list:
            price.date = price.date.strftime('%Y-%m-%d')
            price.deadline = price.deadline.strftime('%Y-%m-%d')
        if 'examine' in request.GET:
            context= {
                'price_list':price_list,
                'prompt':True,
                'prompt_msg':'审核成功！',
            }
        else:
            context = {
                'price_list':price_list,
            }
        return render(request,'examine_price_list.html',context)
    else:
        return render_to_response('permission_error.html')

@login_required(login_url='/user_login/')
def attachment_list(request):
    if request.user.is_staff:
        attachment_list = Attachment.objects.all().order_by('-date')
        for attachment in attachment_list:
            attachment.date = attachment.date.strftime('%Y-%m-%d')
        return render_to_response('attachment_list.html',{'attachment_list':attachment_list,'user':request.user})
    else:
        return render_to_response('permission_error.html')

@login_required(login_url='/user_login/')
def get_attachment(request,id):
    if request.user.is_staff:
        attachment = Attachment.objects.get(id=id)
        file = attachment.file
        list = file.name.split('.')
        file_name = date.today().strftime('%Y%m%d')+'.'+list[1]
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment; filename="%s"'%file_name
        return response
    else:
        return render_to_response('permission_error.html')

def upload_attachment(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect(attachment_list)
        else:
            form = AttachmentForm()
        return render(request, 'upload_attachment.html', {'form': form})
    else:
        return render_to_response('')

def delete_attachment(request,id):
    if request.user.is_staff:
        try:
            attachment = Attachment.objects.get(id=id)
            attachment.delete()
            return redirect(attachment_list)
        except Attachment.DoesNotExist:
            print('attachment does not exist')
    else:
        return render_to_response('permission_error.html')

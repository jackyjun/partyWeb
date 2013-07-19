# Create your views here.
#coding=utf-8
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render,redirect
from django.views.decorators.csrf import csrf_exempt
from member.models import UserStudent,Student
from models import News,Regulation,Notice,Price,StudentPrice
from datetime import *
def get_news(request,id):
    try:
        news = News.objects.get(id=id)
        news.date = news.date.strftime('%Y-%m-%d')
        return render_to_response('news.html',{'news':news})
    except News.DoesNotExist:
        return render_to_response('error.html',{'msg':'news does not exist.'})

def get_notice(request,id):
    try:
        notice = Notice.objects.get(id=id)
        notice.date = notice.date.strftime('%Y-%m-%d')
        return render_to_response('detail.html',{'detail':notice})
    except Notice.DoesNotExist:
        return render_to_response('error.html',{'msg':'notice does not exist.'})

def get_regulation(request,id):
    try:
        regulation = Regulation.objects.get(id=id)
        regulation.date = regulation.date.strftime('%Y-%m-%d')
        return render_to_response('detail.html',{'detail':regulation})
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
    return render_to_response('list.html',{'item_list':news_list,'title':u'新闻动态','type':'news'})

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
    return render_to_response('list.html',{'item_list':notice_list,'title':title,'type':'notice'})

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
    return render_to_response('list.html',{'item_list':regulation_list,'title':u'制度条例','type':'regulation'})

def list_price(request):
    price_list = Price.objects.all().order_by('-deadline')
    list = []
    for price in price_list:
        price_dic = {}
        if price.deadline < date.today():
            flag = -1
        else:
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
    return render_to_response('price_list.html',{'price_list':list})

def apply_price(request,id):
    user = request.user
    if user.is_active:
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        StudentPrice.objects.get_or_create(student_id = student.id,price_id = id)
        return redirect(list_price)
    else:
        return render_to_response('login.html')

def cancel_price(request,id):
    user = request.user
    if user.is_active:
        userStudent = UserStudent.objects.get(user = user)
        student = userStudent.student
        try:
            studentPrice= StudentPrice.objects.get(student_id = student.id,price_id = id)
            studentPrice.delete()
            return redirect(list_price)
        except StudentPrice.DoesNotExist:
            return redirect(list_price)
    else:
        return render_to_response('login.html')

def price_detail(request,id):
    try:
        price = Price.objects.get(id=id)
        return render_to_response('price_detail.html',{'price':price})
    except Price.DoesNotExist:
        return redirect(list_price)

def student_price(request):
    if request.user.is_active:
        student = UserStudent.objects.get(user=request.user).student
        studentPrice_list = StudentPrice.objects.filter(student = student)
        price_dic = {}
        for studentPrice in studentPrice_list:
            price = studentPrice.price
            price.date = price.date.strftime('%Y-%m-%d')
            price.deadline = price.deadline.strftime('%Y-%m-%d')
            price_dic[studentPrice] = price
        print price_dic
        return render_to_response('student_price.html',{'price_dic':price_dic})
    else:
        return render_to_response('login.html')

@csrf_exempt
def examine_price(request,id):
    user = request.user
    if user.is_active:
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
            return redirect(examine_price_list)
    else:
        return render_to_response('login.html')

def examine_price_result(request,id):
    user = request.user
    if user.is_active:
        price = Price.objects.get(id = id)
        price.date = price.date.strftime('%Y-%m-%d')
        studentPrice_list = StudentPrice.objects.filter(price = price)
        student_dic = {}
        for studentPrice in studentPrice_list:
            student_dic[studentPrice] = studentPrice.student
        context ={
            'price': price,
            'student_dic':student_dic,
        }
        return render_to_response('examine_price_result.html',context)
    else:
        return render_to_response('login.html')

def examine_price_list(request):
#examine price list
    if request.user.is_active:
        price_list = Price.objects.all()
        for price in price_list:
            price.date = price.date.strftime('%Y-%m-%d')
            price.deadline = price.deadline.strftime('%Y-%m-%d')
        return render_to_response('examine_price_list.html',{'price_list':price_list})
    else:
        return render_to_response('login.html')
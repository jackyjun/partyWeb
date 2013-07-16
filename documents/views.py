# Create your views here.
#coding=utf-8
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from models import News,Regulation,Notice
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
        return render_to_response('detail.html',{'detail':notice})
    except Notice.DoesNotExist:
        return render_to_response('error.html',{'msg':'notice does not exist.'})

def get_regulation(request,id):
    try:
        regulation = Regulation.objects.get(id=id)
        return render_to_response('detail.html',{'detail':regulation})
    except Regulation.DoesNotExist:
        return render_to_response('error.html',{'msg':'regulation does not exist.'})

def list_news(request,page):
    NEWS_COUNT = 10
    item_list = News.objects.all().order_by('-date')
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

def list_notice(request,page):
    NOTICE_COUNT = 10
    item_list = Notice.objects.all().order_by('-date')
    paginator = Paginator(item_list,NOTICE_COUNT)
    try:
        notice_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notice_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notice_list = paginator.page(paginator.num_pages)
    for notice in notice_list:
        notice.date = notice.date.strftime('%Y-%m-%d')
    return render_to_response('list.html',{'item_list':notice_list,'title':u'通知公告','type':'notice'})

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


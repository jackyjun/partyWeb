# Create your views here.
#coding=utf-8
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render,redirect
from django.views.decorators.csrf import csrf_exempt
from member.models import UserStudent,Student
from models import *
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
    item_list = Regulation.objects.all().order_by('-date').order_by('-id')
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

@login_required(login_url='/user_login/')
def list_price(request):
    price_list = Price.objects.all().order_by('-deadline')
    list = []
    for price in price_list:
        price_dic = {}
        if price.deadline >= date.today():
            if price.status==False:
                try:
                    if request.user.is_active:
                        userStudent = UserStudent.objects.get(user = request.user)
                        student = userStudent.student
                        studentPrice = StudentPrice.objects.get(student_id = student.id,price_id = price.id)
                        if studentPrice.file:
                            flag = 2
                        else:
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
    return render(request,'student_price.html',{'price_dic':price_dic})

@csrf_exempt
@login_required(login_url='/user_login/')
def upload_price_form(request,id):
    if request.method == 'POST':
        try:
            student = UserStudent.objects.get(user=request.user).student
            price = Price.objects.get(id=id)
            student_price = StudentPrice.objects.get(price=price,student=student)
            form = StudentPriceForm(request.POST, request.FILES,instance=student_price)
            if form.is_valid():
                form.save()
                return redirect(list_price)
        except StudentPrice.DoesNotExist:
            return redirect(list_price)
    else:
        student = UserStudent.objects.get(user=request.user).student
        price = Price.objects.get(id=id)
        try:
            student_price = StudentPrice.objects.get(price=price,student=student)
            form = StudentPriceForm(instance=student_price)
            return render(request, 'upload_price_form.html', {'form': form,'id':id})
        except StudentPrice.DoesNotExist:
            return redirect(list_price)

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
def download_price_attachment(request,id,type):
    #price attachment
    try:
        price = Price.objects.get(id=id)
        if int(type)==1:
            file = price.first_file
        elif int(type)==2:
            file = price.second_file
        else:
            return redirect('/price_detail%s/'%id)
        if file:
            list = file.name.split('.')
            file_name = date.today().strftime('%Y%m%d')+'.'+list[1]
            response = HttpResponse(file)
            response['Content-Disposition'] = 'attachment; filename="%s"'%file_name
            return response
        else:
            return redirect('/price_detail/%s'%id)
    except Price.DoesNotExist:
        return redirect('/price_detail/%s'%id)

@login_required(login_url='/user_login/')
def download_price_form(request,id):
    #student price form
    if request.user.is_superuser:
        try:
            student_price = StudentPrice.objects.get(id=id)
            if student_price.file:
                file = student_price.file
                list = file.name.split('.')
                student = student_price.student
                file_name = student.student_id+'.'+list[1]
                response = HttpResponse(file)
                response['Content-Disposition'] = 'attachment; filename="%s"'%file_name
                return response
            else:
                return redirect('/examine_price_list')
        except StudentPrice.DoesNotExist:
            return redirect('/examine_price_list/')
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

@login_required(login_url='/user_login/')
def upload_attachment(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                attachment = form.save(commit=False)
                attachment.publisher = request.user
                attachment.save()
                return redirect(attachment_list)
        else:
            form = AttachmentForm()
        return render(request, 'upload_attachment.html', {'form': form})
    else:
        return render_to_response('permission_error.html')

@login_required(login_url='/user_login/')
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

@csrf_exempt
def add_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return redirect('/list_reply?prompt=True')
    else:
        form = SuggestionForm()
    return render(request, 'add_suggestion.html', {
        'form': form,
    })

@login_required(login_url='/user_login/')
def list_suggestion(request):
    #back
    if request.user.is_superuser:
        suggestion_list = Suggestion.objects.all().order_by('-id').order_by('status')
        for suggestion in suggestion_list:
            suggestion.date = suggestion.date.strftime('%Y-%m-%d %H:%M:%S')
        if 'prompt' in request.GET:
            return render(request, 'list_suggestion.html', {
                'prompt':True,
                'prompt_msg':'回复成功',
                'suggestion_list':suggestion_list,
            })
        else:
            return render(request,'list_suggestion.html',{'suggestion_list':suggestion_list})
    else:
        render_to_response('permission_error.html')

def list_reply(request):
    #user
    suggestion_list = Suggestion.objects.filter(status=True)
    for suggestion in suggestion_list:
        suggestion.date = suggestion.date.strftime('%Y-%m-%d %H:%M:%S')
    if 'prompt' in request.GET:
        return render(request, 'list_reply.html', {
            'suggestion_list':suggestion_list,
            'prompt':True,
            'prompt_msg':'感谢您的建议,请等待管理员回复。',
        })
    return render(request,'list_reply.html',{'suggestion_list':suggestion_list})

@csrf_exempt
@login_required(login_url='/user_login/')
def add_reply(request,id):
    if request.user.is_superuser:
        try:
            if request.method == 'POST':
                content = request.POST['content']
                suggestion = Suggestion.objects.get(id=id)
                if suggestion.status:
                    pass
                else:
                    Reply.objects.get_or_create(user=request.user,content=content,suggestion_id=id)
                    suggestion.status = True
                    suggestion.save()
                return redirect('/list_suggestion?prompt=True')
            else:
                suggestion  = Suggestion.objects.get(id=id)
                return render(request, 'add_reply.html',{'suggestion':suggestion})
        except:
            pass
    else:
        return render_to_response('permission_error.html')

def get_reply(request,id):
    if request.user.is_superuser:
        try:
            suggestion =Suggestion.objects.get(id=id)
            reply = Reply.objects.get(suggestion=suggestion)
            suggestion.date = suggestion.date.strftime('%Y-%m-%d %H:%M:%S')
            reply.date = reply.date.strftime('%Y-%m-%d %H:%M:%S')
            return render(request,'get_reply.html',{'reply':reply,'suggestion':suggestion})
        except:
            pass
    else:
        return render_to_response('permission_error.html')

@csrf_exempt
@login_required(login_url='/user_login/')
def change_reply(request,id):
    if request.user.is_superuser:
        try:
            if request.method == 'POST':
                content = request.POST['content']
                suggestion = Suggestion.objects.get(id=id)
                reply = Reply.objects.get(suggestion=suggestion)
                reply.user = request.user
                reply.content = content
                reply.save()
                return redirect('/list_suggestion?prompt=True')
            else:
                suggestion = Suggestion.objects.get(id=id)
                reply = Reply.objects.get(suggestion=suggestion)
                return render(request, 'change_reply.html',{'suggestion':suggestion,'reply':reply})
        except:
            pass
    else:
        return render_to_response('permission_error.html')
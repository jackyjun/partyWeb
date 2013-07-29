#coding=utf-8
from django.db import models
from django.forms import ModelForm
from member.models import Student

class News(models.Model):
    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = u'新闻'
    title = models.CharField(max_length=200,verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容')
    date = models.DateField(verbose_name=u'日期')
    publisher = models.CharField(max_length=45,verbose_name=u'发布者')
    image = models.ImageField(upload_to='news',verbose_name=u'图片')
    def __unicode__(self):
        return '%s: %s' % (self.date, self.title)

class Notice(models.Model):
    TYPE_CHOICE = (
        (1,u'学院通知'),
        (2,u'组织发展公示'),
    )
    class Meta:
        verbose_name = u'通知公示'
        verbose_name_plural = u'通知公示'
    title = models.CharField(max_length=200,verbose_name=u'标题')
    type = models.IntegerField(max_length=1,verbose_name=u'类型',choices=TYPE_CHOICE)
    content = models.TextField(verbose_name=u'内容')
    date = models.DateField(verbose_name=u'日期')
    publisher = models.CharField(max_length=45,verbose_name=u'发布者')
    def __unicode__(self):
        return '%s: %s' % (self.date, self.title)

class Regulation(models.Model):
    class Meta:
        verbose_name = u'条例'
        verbose_name_plural = u'条例'
    title = models.CharField(max_length=200,verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容');
    date = models.DateField(verbose_name=u'日期');
    publisher = models.CharField(max_length=45,verbose_name=u'发布者')
    def __unicode__(self):
        return '%s: %s' % (self.date, self.title)

class Attachment(models.Model):
    class Meta:
        verbose_name = u'文件'
        verbose_name_plural = u'文件'

    title = models.CharField(max_length=200,verbose_name=u'文件名')
    date = models.DateField(verbose_name=u'上传日期')
    file = models.FileField(upload_to='files',verbose_name=u'文件')
    def __unicode__(self):
        return '%s: %s' % (self.date, self.title)

class Price(models.Model):
    class Meta:
        verbose_name = u'奖项'
        verbose_name_plural = u'奖项'

    title = models.CharField(max_length=200,verbose_name=u'奖项名')
    date = models.DateField(verbose_name=u'发布日期')
    deadline = models.DateField(verbose_name=u'申请截止日期')
    requirement = models.TextField(verbose_name=u'奖项要求',default='',blank=True)
    status = models.BooleanField(verbose_name=u'是否已审核',default=False)
    def __unicode__(self):
        return '%s: %s' % (self.date, self.title)

class StudentPrice(models.Model):
    STATUS_CHOICE = (
        (1,u'未审核'),
        (2,u'未通过'),
        (3,u'通过'),
    )
    student = models.ForeignKey(Student)
    price = models.ForeignKey(Price)
    status = models.IntegerField(max_length=1,choices=STATUS_CHOICE,default=1)
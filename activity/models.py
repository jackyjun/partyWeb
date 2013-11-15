#coding=utf-8
from django.db import models
from member.models import Student
from django.contrib.auth.models import User
from django.forms import ModelForm

class Activity(models.Model):
    TYPE_CHOICE = (
        (0,u'研究生会活动'),
        (1,u'团组织活动'),
        (2,u'党组织生活'),
        (3,u'其他活动'),
    )
    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = u'活动'
    title = models.CharField(max_length=200,verbose_name=u'标题')
    type = models.IntegerField(max_length=1,verbose_name=u'活动类型',choices=TYPE_CHOICE)
    publisher = models.ForeignKey(User,verbose_name=u'活动发布者')
    start_time = models.DateField(verbose_name=u'活动开始日期')
    end_time = models.DateField(verbose_name=u'活动结束日期')
    deadline = models.DateField(verbose_name=u'报名截止日期')
    content = models.TextField(verbose_name=u'内容')
    status = models.BooleanField(verbose_name=u'是否已审核')
    def __unicode__(self):
        return '%s: %s' % (self.start_time, self.title)

class StudentActivity(models.Model):
    STATUS_CHOICE = (
        (0,u'未参与'),
        (1,u'参与者'),
        (2,u'组织者'),
    )
    class Meta:
        verbose_name = u'学生活动情况'
        verbose_name_plural = u'学生活动情况'
    student = models.ForeignKey(Student,verbose_name=u'学生')
    activity = models.ForeignKey(Activity,verbose_name=u'活动名')
    status = models.IntegerField(max_length=1,choices=STATUS_CHOICE,default=0,verbose_name=u'参与情况')
    award = models.CharField(max_length=200,null=True,default='',blank=True,verbose_name=u'获奖情况')
    def __unicode__(self):
        return '%s %s: %s %s' % (self.student.student_id,self.student.name, self.activity.title,self.get_status_display())

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ('status','publisher')
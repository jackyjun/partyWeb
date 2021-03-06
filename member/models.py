#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class PartyBranch(models.Model):
    class Meta:
        verbose_name = u'党支部'
        verbose_name_plural = u'党支部'

    name = models.CharField(max_length=100,verbose_name=u'党支部名称')
    def __unicode__(self):
        return '%s' %self.name

class Student(models.Model):
    GENDER_CHOICE = (
        (0, u'男'),
        (1, u'女'),
    )
    POLITICAL_STATUS_CHOICE = (
        (0,u'群众'),
        (1,u'共青团员'),
        (2,u'预备党员'),
        (3,u'正式党员'),
    )
    SUBJECT_CHOICE = (
        (0,u'学术型硕士'),
        (1,u'专业型硕士'),
        (2,u'联合培养型硕士'),
        (3,u'博士'),
    )
    TRAINING_CHOICE = (
        (0,'统分'),
        (1,'委培'),
    )
    class Meta:
        verbose_name = u'学生信息'
        verbose_name_plural = u'学生信息'

    student_id = models.CharField(max_length=20,null=True,default='',verbose_name=u'学号',blank=True)
    name = models.CharField(max_length=100,null=True,default='',verbose_name=u'姓名',blank=True)
    subject = models.IntegerField(max_length=1,default=0,null=True,choices=SUBJECT_CHOICE,verbose_name=u'学科类型',blank=True)
    training = models.IntegerField(max_length=1,default=0,null=True,choices=TRAINING_CHOICE,verbose_name=u'培养类型',blank=True)
    major = models.CharField(max_length=100,verbose_name=u'专业',null=True,default='',blank=True)
    professor = models.CharField(max_length=100,verbose_name=u'导师',null=True,default='',blank=True)
    gender = models.IntegerField(max_length=1,null=True,default=0,choices=GENDER_CHOICE,verbose_name=u'性别',blank=True)
    phone = models.CharField(max_length=100,verbose_name=u'手机',null=True,default='',blank=True)
    dormitory = models.CharField(max_length=100,verbose_name=u'寝室',null=True,default='',blank=True)
    laboratory = models.CharField(max_length=100,verbose_name=u'实验室',null=True,default='',blank=True)
    seat_number = models.CharField(max_length=100,verbose_name=u'座位号',null=True,default='',blank=True)
    party_branch = models.ForeignKey(PartyBranch,verbose_name=u'所属党支部',blank=True,default=1,null=True)
    political_status = models.IntegerField(max_length=1,choices=POLITICAL_STATUS_CHOICE,verbose_name=u'政治面貌',null=True,default=0,blank=True)
    apply_party_time = models.DateField(verbose_name=u'入党时间',null=True,blank=True)
    join_party_time = models.DateField(verbose_name=u'转正时间',null=True,blank=True)
    duty = models.CharField(max_length=100,verbose_name=u'职务',null=True,default='',blank=True)
    #birthday = models.DateField(verbose_name=u'出生年月', null=True,blank=True)
    #degree = models.CharField(max_length=100,verbose_name=u'学位',null=True,default='',blank=True)
    #place = models.CharField(max_length=100,verbose_name=u'生源地',null=True,default='',blank=True)
    #email = models.CharField(max_length=100,verbose_name=u'电子邮箱',null=True,default='',blank=True)
    #qq_number = models.CharField(max_length=100,verbose_name=u'QQ',null=True,default='',blank=True)
    #league_member = models.BooleanField(max_length=1,verbose_name=u'是否团员',default=True,blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.student_id, self.name)

class UserStudent(models.Model):
    student = models.ForeignKey(Student)
    user = models.ForeignKey(User)

class StudentAssessment(models.Model):
    class Meta:
        verbose_name = u'党员考核'
        verbose_name_plural = u'党员考核'

    student = models.ForeignKey(Student)
    grade = models.CharField(verbose_name=u'考核等级',max_length=20)
    date = models.DateField(verbose_name=u'考核时间')

    def __unicode__(self):
        return '%s,%s%s:%s' % (self.date,self.student.student_id, self.student.name,self.grade)

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('phone','professor','dormitory')

from django import forms
#import xls
class ImportXlsForm(forms.Form):
    file  = forms.FileField()



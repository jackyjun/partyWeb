#coding=utf-8
from django.db import models
from django.forms import ModelForm

class News(models.Model):
    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = u'新闻'
    title = models.CharField(max_length=200,verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容');
    date = models.DateField(verbose_name=u'日期');
    publisher = models.CharField(max_length=45,verbose_name=u'发布者')
    image = models.ImageField(upload_to='news',verbose_name=u'图片')
    def __unicode__(self):
        return '%s: %s' % (self.date, self.title)

class Notice(models.Model):
    class Meta:
        verbose_name = u'通知'
        verbose_name_plural = u'通知'
    title = models.CharField(max_length=200,verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容');
    date = models.DateField(verbose_name=u'日期');
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
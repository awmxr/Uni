from django.db import models
from django.db import models
from django.utils import timezone
import datetime


class Student(models.Model):
    uni_choices = (
        ('------------------------------------------------------------------------------','------------------------------------------------------------------------------'),
        ('تهران','تهران'),
        ('مازندران','مازندران'),
        ('اصفهان','اصفهان'),
        ('امیرکبیر','امیر کبیر'),
        ('صنعتی شریف','صنعتی شریف'),
        ('شهید بهشتی','شهید بهشتی'),
        ('صنعتی اصفهان','صنعتی اصفهان'),
        ('علم و صنعت','علم و صنعت'),
        ('خواجه نصیر','خواجه نصیر'),
        ('شیراز','شیراز'),
        ('نوشیروانی','نوشیروانی'),
        ('تبریز','تبریز'),
    )
    college_choices = (
        ('------------------------------------------------------------------------------','------------------------------------------------------------------------------'),
        ('فنی مهندسی','فنی مهندسی'),
        ('علوم پایه','علوم پایه'),
        ('اقتصاد','اقتصاد'),
        ('علوم سیاسی','علوم سیاسی'),
        ('اقیانوس','اقیانوس'),
        ('شیمی','شیمی'),
    )
    live_choices = (
        ('------------------------------------------------------------------------------','------------------------------------------------------------------------------'),
        ('تهران','تهران'),
        ('کرج','کرج'),
        ('مازندران','مازندران'),
        ('گیلان','گیلان'),
        ('قم','قم'),
        ('مرکزی','مرکزی'),
        ('تبریز','تبریز'),
        ('خوزستان','خوزستان'),
        ('خراسان رضوی','خراسان رضوی'),
        ('البرز','البرز'),
        ('کرمان','کرمان'),
        ('شیزار','شیراز'),
        ('اصفهان','اصفهان'),
    )
    field_choices = (
        ('------------------------------------------------------------------------------','------------------------------------------------------------------------------'),
        ('مهندسی کامپیوتر','مهندسی کامپیوتر'),
        ('مهندسی برق','مهندسی برق'),
        ('مهندسی عمران','مهندسی عمران'),
        ('مهندسی مکانیک','مهندسی مکانیک'),
        ('مهندسی شیمی','مهندسی شیمی'),
        ('مهندسی شهرسازی','مهندسی شهرسازی'),
        ('علوم کامپیوتر','علوم کامپیوتر'),
        ('ریاضی','ریاضی'),
        ('فیزیک','فیریک'),
        ('شیمی','شیمی'),
        ('معماری','معماری'),
        ('اقتصاد','اقتصاد'),
        ('علوم سیاسی','علوم سیاسی'),
        ('هنر','هنر'),
        ('معارف','معارف'),
        ('مدیریت','مدیریت'),
    )
    enter_year_choices = (
        ('------------------------------------------------------------------------------','------------------------------------------------------------------------------'),
        ('1400','1400'),
        ('1399','1399'),
        ('1398','1398'),
        ('1397','1397'),
        ('1396','1396'),
        ('1395','1395'),
        ('1394','1394'),
        ('1393','1393'),
        ('1392','1392'),
        ('1391','1391'),
    )
    religion_choices = (
        ('------------------------------------------------------------------------------','------------------------------------------------------------------------------'),
        ('شیعه 12 امامی','شیعه 12 امامی'),
        ('شیعه 7 امامی','شیعه 7 امامی'),
        ('مسیحی','مسیحی'),
        ('زرتشت','زرتشت'),
        ('بهایی','بهایی'),
        ('یهودی','یهودی'),
    )
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    melli_code = models.CharField(max_length=200)
    enter_year = models.CharField(max_length=200, choices  = enter_year_choices)
    uni = models.CharField(max_length=200, choices = uni_choices)
    College = models.CharField(max_length=200 , choices = college_choices)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    field = models.CharField(max_length=200, choices = field_choices)
    student_live = models.CharField(max_length=200, choices = live_choices)
    parents_phone = models.CharField(max_length=200)
    religion = models.CharField(max_length=200 , choices = religion_choices)

    
    # birthday = models.DateTimeField('birthday')


    def __str__(self):
        return self.name +' ' +  self.last_name
    

class Admin(models.Model):
    Admin_username = models.CharField(max_length=200)
    admin_name = models.CharField(max_length=200)
    admin_last_name = models.CharField(max_length=200)
    admin_password = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.admin_name +' ' +  self.admin_last_name
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Exter(models.Model):
    exter_name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)

    def __str__(self):
        return self.exter_name
    

# Create your models here.

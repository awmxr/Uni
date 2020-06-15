from django.db import models
from django.utils import timezone
from datetime import datetime , date
import datetime
from . import choices


class Student(models.Model):
    
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    melli_code = models.CharField(max_length=200)
    enter_year = models.CharField(max_length=200)
    uni = models.CharField(max_length=200)
    College = models.CharField(max_length=200 )
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    field = models.CharField(max_length=200)
    student_live = models.CharField(max_length=200)
    parents_phone = models.CharField(max_length=200)
    religion = models.CharField(max_length=200 )
    public_date = models.DateTimeField(null = True)
    login_date = models.DateTimeField(null = True) 
    birthday = models.DateField(blank = True , null = True) 
    login_times = models.CharField(max_length = 10000) 
    grade = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    activate = models.BooleanField(default = True)
    online = models.BooleanField(default = False)
    def __str__(self):
        return self.name +' ' +  self.last_name

    

class Admin(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    public_date = models.DateTimeField(null = True)
    login_date = models.DateTimeField(null = True)
    birthday = models.DateTimeField(null = True) 
    login_times = models.CharField(max_length = 10000) 
    online = models.BooleanField(default = False)
    College = models.CharField(max_length=2000, choices= choices.college_choices)
    field = models.CharField(max_length=200)

    def __str__(self):
        return self.name +' ' +  self.last_name
    
    

class Exter(models.Model):
    exter_name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)

    def __str__(self):
        return self.exter_name


class Exter2(models.Model):
    username = models.CharField(max_length=200)
    ostad = models.CharField(max_length=200)
    dars = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    goruh = models.CharField(max_length=200)


    def __str__(self):
        return self.ostad + '--' + self.dars    

class Ostad(models.Model) :
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    melli_code = models.CharField(max_length=200)
    uni = models.CharField(max_length=200)
    College = models.CharField(max_length=200 )
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    religion = models.CharField(max_length=200 )
    public_date = models.DateTimeField(null = True)
    login_date = models.DateTimeField(null = True) 
    birthday = models.DateField(blank = True , null = True) 
    login_times = models.CharField(max_length = 10000) 
    activate = models.BooleanField(default = True)
    online = models.BooleanField(default = False)
    grade = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    dars1 = models.CharField(max_length=200)
    dars2 = models.CharField(max_length=200)
    dars3 = models.CharField(max_length=200)
    dars4 = models.CharField(max_length=200)
    
    def __str__ (self):
        return self.name + " " + self.last_name
class Elam(models.Model):
    username = models.CharField(max_length=200)
    ostad = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    dars = models.CharField(max_length=200)
    capacity = models.CharField(max_length=200)
    time = models.CharField(max_length=1000)
    public_date = models.DateTimeField(null = True)
    phone = models.CharField(max_length=200)
    goruh = models.CharField(max_length=1000)
    dascode = models.CharField(max_length=1000)
    
    def __str__ (self):
        return self.ostad+ "--" + self.dars


class Klass(models.Model):
    number = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    floor = models.CharField(max_length=200,blank = True)
    public_date = models.DateTimeField(null = True)
    t01 = models.CharField(max_length=200,blank = True)
    t02 = models.CharField(max_length=200,blank = True)
    t03 = models.CharField(max_length=200,blank = True)
    t04 = models.CharField(max_length=200,blank = True)
    t05 = models.CharField(max_length=200,blank = True)
    t11 = models.CharField(max_length=200,blank = True)
    t12 = models.CharField(max_length=200,blank = True)
    t13 = models.CharField(max_length=200,blank = True)
    t14 = models.CharField(max_length=200,blank = True)
    t15 = models.CharField(max_length=200,blank = True)
    t21 = models.CharField(max_length=200,blank = True)
    t22 = models.CharField(max_length=200,blank = True)
    t23 = models.CharField(max_length=200,blank = True)
    t24 = models.CharField(max_length=200,blank = True)
    t25 = models.CharField(max_length=200,blank = True)
    t31 = models.CharField(max_length=200,blank = True)
    t32 = models.CharField(max_length=200,blank = True)
    t33 = models.CharField(max_length=200,blank = True)
    t34 = models.CharField(max_length=200,blank = True)
    t35 = models.CharField(max_length=200,blank = True)
    t41 = models.CharField(max_length=200,blank = True)
    t42 = models.CharField(max_length=200,blank = True)
    t43 = models.CharField(max_length=200,blank = True)
    t44 = models.CharField(max_length=200,blank = True)
    t45 = models.CharField(max_length=200,blank = True)
    def __str__ (self):
        return self.floor + "--" + self.number


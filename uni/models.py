from django.db import models
from django.db import models
from django.utils import timezone
from datetime import datetime , date
import datetime


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

    def __str__(self):
        return self.name +' ' +  self.last_name
    
    

class Exter(models.Model):
    exter_name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)

    def __str__(self):
        return self.exter_name
    

# Create your models here.

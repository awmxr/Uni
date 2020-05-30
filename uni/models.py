from django.db import models
from django.db import models
from django.utils import timezone
import datetime


class Student(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    melli_code = models.CharField(max_length=200)
    enter_year = models.CharField(max_length=200)
    uni = models.CharField(max_length=200)
    College = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    field = models.CharField(max_length=200)
    student_live = models.CharField(max_length=200)
    parents_phone = models.CharField(max_length=200)
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

from django.db import models
from django.db import models
from django.utils import timezone
import datetime

class Student(models.Model):
    student_username = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    student_last_name = models.CharField(max_length=200)
    student_password = models.CharField(max_length=200)
    student_phone = models.CharField(max_length=11)
    student_field = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def __str__(self):
        return self.student_name +' ' +  self.student_last_name
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

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

    def __str__(self):
        return self.exter_name
    

# Create your models here.

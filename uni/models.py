from django.db import models
from django.db import models
from django.utils import timezone
import datetime

class student(models.Model):
    student_name = models.CharField(max_length=200)
    student_last_name = models.CharField(max_length=200)
    student_password = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def __str__(self):
        return self.student_name +' ' +  self.student_last_name
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Admin(models.Model):
    admin_name = models.CharField(max_length=200)
    admin_last_name = models.CharField(max_length=200)
    admin_password = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.admin_name +' ' +  self.admin_last_name
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

# Create your models here.

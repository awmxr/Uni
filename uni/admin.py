from django.contrib import admin
from .models import Student,Admin,Exter,Ostad
# Register your models here.
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Exter)
admin.site.register(Ostad)
admin.site.register(Student.History)
from passlib.hash import oracle10
from .models import Student,Admin,Exter
import datetime as dt
# s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
# if not s1:
#     s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()

def MakeCookie(s1):
    d = str(s1.username) + str(s1.password) + str(s1.birthday) + str(s1.public_date) + 'Amir' + 'mohsen' + str(s1.login_times) + str(s1.login_date)
    x = oracle10.hash(d,user = s1.username)
    return x

def CheckCookie(s1,cooke):
    if str(MakeCookie(s1)) == str(cooke):
        return True
    else:
        # errorr = 'اجازه دسترسی ندارید'
        return False

    

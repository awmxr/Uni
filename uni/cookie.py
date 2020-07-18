from passlib.hash import oracle10
from .models import Student,Admin2
import datetime as dt
import re
from django.utils import timezone


# def checktime(user):
#     if dt.datetime.now() - user.login_date > dt.timedelta(min = 15):
#         return False
#     else:
#         return True


def MakeCookie(user):
    d = 'Amir' + str(user.username)  + str(user.public_date) + 'Amir' + 'uni' +'mohsen'+'21122112'+ str(user.login_times) + str(user.login_date) + 'mohsen'
    x = oracle10.hash(d,user = user.username)
    return str(x)

def CheckCookie(user,cooke):
    if str(MakeCookie(user)) == str(cooke) :

        x = timezone.now()
        z = user.login_date2
        y = z + dt.timedelta(minutes=10)
        if x >= y :
            return False
        else:
            user.login_date2 = timezone.now()
            user.save()
            return True

    else:
        # errorr = 'اجازه دسترسی ندارید'
        return False



def starfunc(a):
    b3 = re.search(r'\b +\b',a)
    d3 = re.search(r'^ *',a)
    g3 = re.search(r' *$',a)
    g4 = re.search('\d+$',a)

    if b3:
        a = re.sub(r'\b +\b',' ',a)
    if d3:
        a = re.sub(r'^ *','',a)
    if g3:
        a = re.sub(r' +$',' ',a)
    if g4:
        a += ' '
    
    return a


    
# s1 = Student.objects.filter(username = request.user.username).first()
#         cookie  = str(request.COOKIES.get('access'))

#         if CheckCookie(s1,cookie) and requenst.user.au:
#             
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))

    

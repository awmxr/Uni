from passlib.hash import oracle10
from .models import Student,Admin2
import datetime as dt


# def checktime(user):
#     if dt.datetime.now() - user.login_date > dt.timedelta(min = 15):
#         return False
#     else:
#         return True


def MakeCookie(user):
    d = 'Amir' + str(user.username) + str(user.birthday) + str(user.public_date) + 'Amir' + 'uni' +'mohsen'+'21122112'+ str(user.login_times) + str(user.login_date) + 'mohsen'
    x = oracle10.hash(d,user = user.username)
    return str(x)

def CheckCookie(user,cooke):
    if str(MakeCookie(user)) == str(cooke) :
        return True
    else:
        # errorr = 'اجازه دسترسی ندارید'
        return False



# s1 = Student.objects.filter(username = request.user.username).first()
#         cookie  = str(request.COOKIES.get('access'))

#         if CheckCookie(s1,cookie) and requenst.user.au:
#             
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))

    

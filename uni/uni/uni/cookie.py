from passlib.hash import oracle10
from .models import Student,Admin,Exter
import datetime as dt
# s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
# if not s1:
#     s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()

def MakeCookie(user):
    d = 'Amir' + str(user.username) + str(user.password) + str(user.birthday) + str(user.public_date) + 'Amir' + 'uni' +'mohsen'+'21122112'+ str(user.login_times) + str(user.login_date) + 'mohsen'
    x = oracle10.hash(d,user = user.username)
    return x

def CheckCookie(user,cooke):
    if str(MakeCookie(user)) == str(cooke):
        return True
    else:
        # errorr = 'اجازه دسترسی ندارید'
        return False



# s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
#         cookie  = str(request.COOKIES.get('access'))

#         if CheckCookie(s1,cookie):
#             
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))

    

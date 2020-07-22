from passlib.hash import oracle10
# from .models import Student,Admin2
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





def manfifunc(a):
    b3 = re.search(r'[v]+',a)
    d3 = re.search(r'^v*',a)
    g3 = re.search(r'v*$',a)
    g4 = re.search('l+$',a)

    if b3:
        
        a = re.sub(r'[v]+','v',a)
    if d3:
        a = re.sub(r'^v*','',a)
    if g3:
        a = re.sub(r'v+$','v',a)
    if g4:
        a += '-'
    
    return a
# a = 'l8,i31 1 ilvvl9,i2 ilv'
# b = manfifunc(a)
# print(b)


def replacel(a,c,d):
    b = re.search(fr'l{c},i(\s|\d)+il',a)
    if b:
        # print('aaaaaaa')
        a = re.sub(fr'l{c},i(\s|\d)+il','',a)
        if d == '':
            pass
        else:
            a += 'v' + f'l{c},i{d}il' + 'v'
    else:
        a += 'v' + f'l{c},i{d}il' + 'v'
    
    return a
 
# a = 'l8,i1 ilv'
# b = replacel(a,8,'')
# print(b)


def checktime(a,c):

    b = re.search(fr'l{c},i(\s|\d)+il',a)
    if b:
        b = b.group()
        b = b.replace('l','')
        b = re.sub(fr'{c},','',b)
        b = b.replace('i','')
        b = starfunc(b)
        b2 = b.split(' ')
        return b2
    else:
        return []


def disapledtime(a,c):
    
    b = re.search(fr'l{c},i(\s|\d)+il',a)
    b2 = []
    b22 = []
    if b:
        
        b2 = a.replace(b.group(),'')
        b2 = b2.replace('v','')
        b2 = b2.replace('l','')
        b2 = b2.replace('i','')
        b2 = re.sub('\d+,','',b2)
        # b2 = starfunc(b2)
        b22 = b2.split(' ')
    elif not b:
        b2 = a.replace('v','')
        b2 = b2.replace('l','')
        b2 = b2.replace('i','')
        b2 = re.sub('\d+,','',b2)
        b22 = b2.split(' ')
    return b22
# a = 'l8,i31 32 ilvl9,i2 ilv'
# b = disapledtime(a,8)
# print(b)

def vahedtime(a):
    b = a.split('v')
    if '' in b:
        b.remove('')
    finalstr = ''
    for i in b:
        i = i.replace('l','')
        i = i.replace('i','')
        j = i.split(',')
        j2 = j[1].split(' ')
        print(j2)
        for l in j2:
            finalstr += ' ' + f'{j[0]},{l}' + ' '
    finalstr = starfunc(finalstr)
    return finalstr


def vahedtime2(a):
    a = vahedtime(a)
    b = a.split(' ')
    finallist = []
    if '' in b:
        b.remove('')
    for i in b:
        j = i.split(',')
        if '' in j:
            j.remove('')
        finallist.append(j)
    return finallist
        
    
def replaceii(a):
    f = re.sub(fr'l\d+,iil','',a)
    return f



    
# s1 = Student.objects.filter(username = request.user.username).first()
#         cookie  = str(request.COOKIES.get('access'))

#         if CheckCookie(s1,cookie) and requenst.user.au:
#             
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))

    

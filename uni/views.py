from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin2, Ostad,Elam,Klass,Account,Vahed,Darkhast,Eteraz,Leader,Boss
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,sabtform,ChangeForm,ChangePass,Change2Form,ChangePass2,sabtform2,ElamForm,KlassForm,EntekhabForm,sabtform3,sabtform4
from django.contrib import messages
from passlib.hash import oracle10
from . import choices
from django import forms
import datetime as dt
from .cookie import CheckCookie,MakeCookie,starfunc
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.template.defaulttags import register
import re
from persiantools.jdatetime import JalaliDateTime

def logout2(user):
    user.login_date = None
    user.login_date2 = None
    user.online = False
    user.save()
    response = HttpResponseRedirect(reverse('uni:home'))
    response.set_cookie('access',None)


def page_logout(request):
    try:
        if request.method == "POST":
            user = request.user
            if user.is_student:
                s = Student.objects.filter(username = user.username).first()
                s.login_date = None
                s.login_date2 = None
                s.online = False
                s.save()
            if user.is_admin2:
                a = Admin2.objects.filter(username = user.username)
                a.login_date = None
                a.login_date2 = None
                a.online = False
            if user.is_ostad:
                o = Ostad.objects.filter(username = user.username)
                o.login_date = None
                o.login_date2 = None
                o.online = False
                
            logout(request)
            
            response = HttpResponseRedirect(reverse('uni:home'))
            response.set_cookie('access',None)
            return response
    except:
        response = HttpResponseRedirect(reverse('uni:home'))
        response.set_cookie('access',None)
        return response
        
gb = 0 #use for message: if gb == 1: message is exist


class HomeView(generic.TemplateView):
    template_name = 'uni/home.html'
    def get(self, request):
        
        global gb
        if gb == 1:
            messages.success(request, '.پسوورد با موفقیت تغییر کرد لطفا دوباره وارد شوید')
            gb = 0

        response = render(request,self.template_name,{})
        return response

class AboutusView(generic.TemplateView):
    template_name = 'uni/aboutus.html'
    def get(self, request):
        response = render(request,self.template_name,{})
        return response
        

class PageView(generic.TemplateView):#student page
    
    template_name = 'uni/page.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated :
            return render(request,self.template_name,{'student':s})
        
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class LeaderView(generic.TemplateView):#student page
    
    template_name = 'uni/leader.html'
    
    def get(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(led,cookie) and request.user.is_authenticated :
            return render(request,self.template_name,{'leader':led})
        
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))


class BossView(generic.TemplateView):#student page
    
    template_name = 'uni/boss.html'
    
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated :
            return render(request,self.template_name,{'boss':bs})
        
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))

            

class Page2View(generic.TemplateView):#admin page
    
    template_name = 'uni/page2.html'
    
    
    def get(self,request,admin_id):
        
        # messages.success(request, 'Email sent successfully.')
        a = Admin2.objects.get(pk = admin_id)
        Admins = Admin2.objects.all()
        Students = Student.objects.all()
        cookie  = str(request.COOKIES.get('access'))
        d = CheckCookie(a,cookie)
        if d and request.user.is_authenticated:
            return render(request,self.template_name,{'admin':a,'Admins':Admins,'Students':Students})
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class Page3View(generic.TemplateView):#ostad page
    
    template_name = 'uni/page3.html'
    
    def get(self,request,ostad_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        w = Elam.objects.filter(username = os.username ,time = '').first()
        if w and w.time == '':
            w.delete()
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            return render(request,self.template_name,{'ostad':os})
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
  



class AboutSView(generic.TemplateView):#student info page
    
    template_name = 'uni/aboutS.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class AboutS3View(generic.TemplateView):#student info page in ostad
    
    template_name = 'uni/aboutS3.html'
    
    def get(self,request,ostad_id,student_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'student':s,'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

    
class AboutS2View(generic.TemplateView):#student info page in admin
    
    template_name = 'uni/aboutS2.html'
    
    def get(self,request,admin_id,student_id):
        
        a = Admin2.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            context = {'student':s,'admin':a}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

    
class ChangeView(generic.TemplateView):#change info by student
    
    template_name = 'uni/change.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            
            form = ChangeForm(instance=s)
            form.student = s
            context = {'form':form,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            form = ChangeForm(request.POST,instance=s)
            if form.is_valid():
                form.save()
                
                del form
                message = 'تغییرات با موفقیت اعمال شد'
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
            
            elif not form.is_valid():
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'student':s,'error_message':error_message}
                return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
            



v = 0
class CreateView(generic.TemplateView):#create student by admin
    
    template_name = 'uni/create.html'
    
    
    def get(self,request ,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            form = sabtform()
            context = {'form':form,'admin':a}
            return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        global v
        # v = 0
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform(request.POST)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
                nam = form.cleaned_data['username']
                users = Account.objects.all()
                for i in users:
                    
                    if i.username == nam:
                        error_message = f'این شماره دانشجویی در حال حاضر وجود دارد'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request ,self.template_name,context)
                
                if form.cleaned_data['College'] == 'فنی مهندسی'  and v != 2:
                    v = 2
                    form.fields['field'].widget = forms.Select(choices= choices.field1_choices)
                    context = {'form':form,'admin':a,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم پایه'  and v != 3:
                    v = 3
                    form.fields['field'].widget = forms.Select(choices= choices.field2_choices)
                    context = {'form':form,'admin':a,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم اقتصادی و اداری' and v != 4:
                    v = 4
                    form.fields['field'].widget = forms.Select(choices= choices.fileld3_choices)
                    context = {'form':form,'admin':a,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم سیاسی'  and v != 5:
                    v = 5
                    form.fields['field'].widget = forms.Select(choices= choices.fileld4_choices)
                    context = {'form':form,'admin':a,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم دریایی'  and v != 6:
                    v = 6
                    form.fields['field'].widget = forms.Select(choices= choices.fileld5_choices)
                    context = {'form':form,'admin':a,}
                    return render(request ,self.template_name,context)
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                v = 0
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                        # v = 0
                        error_message = 'لطفا فرم را کامل پر کنید'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request ,self.template_name,context)
                v = 1
                date1 = request.POST.get('date')
                form.save()
                Student.objects.filter(username = z).update(birthday = date1)
                Student.objects.filter(username = z).update(login_times = '0')
                Student.objects.filter(username = z).update(public_date = dt.datetime.now())
                user = Account.objects.create_user(username = z,password = form.cleaned_data['password'])
                user.is_student = True
                user.save()
                
                
                # v = 0 
                x = Student.objects.filter(username = z).update(password = y)
                form = sabtform()
                message = 'دانشجو با موفقیت ثبت شد'
                context = {'form':form,'admin':a}
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
        

        
        
  
class LoginView(generic.TemplateView):#login page
    
    # model = Student
    template_name = 'uni/login.html'

    def get(self , request):

        form = Loginform()
        context = {'form' : form}
        response = render(request,self.template_name,context)
        return response
        
    def post(self,request):
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username , password = password)
            if not user:
                error_message = "شماره کاربری یا رمز عبور غلط است"
                context = {'form' : form ,'error_message':error_message }
                return render(request ,'uni/login.html',context)
            if user.is_student : 
                s = Student.objects.filter(username = user.username).first()
                response = HttpResponseRedirect(reverse('uni:page',args = [s.id]))
                login(request,user)
                s.login_date = dt.datetime.now()
                s.login_date2 = dt.datetime.now()
                s.login_times = str(int(s.login_times)+1)
                s.online = True
                s.save()
                h = Student.objects.filter(username = form.cleaned_data['username']).first()
                response.set_cookie('access',MakeCookie(h))
                return response
            if user.is_admin2 : 
                a = Admin2.objects.filter(username = user.username).first()
                response = HttpResponseRedirect(reverse('uni:page2',args = [a.id]))
                login(request,user)
                a.login_date = dt.datetime.now()
                a.login_date2 = dt.datetime.now()
                a.login_times = str(int(a.login_times)+1)
                a.online = True
                a.save()
                h = Admin2.objects.filter(username = form.cleaned_data['username']).first()
                response.set_cookie('access',MakeCookie(h))
                return response
            if user.is_ostad : 
                os = Ostad.objects.filter(username = user.username).first()
                response = HttpResponseRedirect(reverse('uni:page3',args = [os.id]))
                login(request,user)
                os.login_date = dt.datetime.now()
                os.login_date2 = dt.datetime.now()
                os.login_times = str(int(os.login_times)+1)
                os.online = True
                os.save()
                h = Ostad.objects.filter(username = form.cleaned_data['username']).first()
                response.set_cookie('access',MakeCookie(h))
                return response  
            if user.is_leader : 
                led = Leader.objects.filter(username = user.username).first()
                response = HttpResponseRedirect(reverse('uni:leader',args = [led.id]))
                login(request,user)
                led.login_date = dt.datetime.now()
                led.login_date2 = dt.datetime.now()
                led.login_times = str(int(led.login_times)+1)
                led.online = True
                led.save()
                h = Leader.objects.filter(username = form.cleaned_data['username']).first()
                response.set_cookie('access',MakeCookie(h))
                return response
            if user.is_boss : 
                bs = Boss.objects.filter(username = user.username).first()
                response = HttpResponseRedirect(reverse('uni:boss',args = [bs.id]))
                login(request,user)
                bs.login_date = dt.datetime.now()
                bs.login_date2 = dt.datetime.now()
                bs.login_times = str(int(bs.login_times)+1)
                bs.online = True
                bs.save()
                h = Boss.objects.filter(username = form.cleaned_data['username']).first()
                response.set_cookie('access',MakeCookie(h))
                return response 
            # else:
            #     error_message = 'شماره کاربری یا رمز عبور غلط است'
            #     return render(request,self.template_name,{'form' : form ,'error_message':error_message})

                      
        error_message = 'لطفا فرم را کامل پر کنید'
        return render(request,self.template_name,{'form' : form ,'error_message':error_message})

class ChangePassView(generic.TemplateView):#change password by student
    template_name = 'uni/changepass.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            form = ChangePass()
            context = {'student':s,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            form = ChangePass(request.POST)
            if form.is_valid():
                user = request.user
                if oracle10.hash(form.cleaned_data['pass1'],user = s.username) == s.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        s.password = oracle10.hash(form.cleaned_data['pass3'],user = s.username)
                        s.save()
                        user.set_password(form.cleaned_data['pass3'])
                        user.save()
                        global gb
                        gb = 1
                        logout2(s)
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'student':s,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'student':s,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'student':s,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))


class ChangePassView2(generic.TemplateView):#change password by admin
    template_name = 'uni/changepass2.html'
    
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = ChangePass()
            context = {'admin':a,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            form = ChangePass(request.POST)
            if form.is_valid():
                user = request.user
                if oracle10.hash(form.cleaned_data['pass1'],user = a.username) == a.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        a.password = oracle10.hash(form.cleaned_data['pass3'],user = a.username)
                        a.save()
                        user.set_password(form.cleaned_data['pass3'])
                        user.save()
                        global gb
                        gb = 1
                        logout2(a)
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'admin':a,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'admin':a,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class ChangePassView4(generic.TemplateView):#change password by ostad
    template_name = 'uni/changepass4.html'
    
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            form = ChangePass()
            context = {'ostad':os,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            form = ChangePass(request.POST)
            if form.is_valid():
                user = request.user
                if oracle10.hash(form.cleaned_data['pass1'],user = os.username) == os.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        os.password = oracle10.hash(form.cleaned_data['pass3'],user = os.username)
                        os.save()
                        user.set_password(form.cleaned_data['pass3'])
                        user.save()
                        global gb
                        gb = 1
                        logout2(os)
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'ostad':os,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'ostad':os,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


class StudentsView(generic.TemplateView):#student list in admin
    template_name = 'uni/students.html'
    
   
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        Students = Student.objects.filter(College = a.College,uni = a.uni)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            context = {'admin':a,'Students':Students}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,admin_id):
        Students = Student.objects.all()
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            students = Student.objects.filter(College = a.College,uni = a.uni)
            s = None
            for i in students:
                if i.name+' '+i.last_name == c:
                    s = Student.objects.filter(name = i.name , last_name = i.last_name).first()
                    break
            

            if not s:
                s = Student.objects.filter(username = c).first()
            context = {'admin':a,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
            return response
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

class Student1View(generic.TemplateView):#student profile in admin
    template_name = 'uni/student1.html'
    
    
    def get(self,request,admin_id,student_id):
        s = Student.objects.get(pk = student_id)
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            global gb
            if gb == 1:
                messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                gb = 0
            context = {'admin':a,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class Student3View(generic.TemplateView):#student profile in ostad
    template_name = 'uni/student3.html'
    
    def get(self,request,ostad_id,student_id):
        s = Student.objects.get(pk = student_id)
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


    
class Students3View(generic.TemplateView):#student list in ostad
    template_name = 'uni/students3.html'
    
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        Students = Student.objects.filter(uni = os.uni)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os,'Students':Students}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,ostad_id):
        Students = Student.objects.all()
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            students = Student.objects.filter(uni = os.uni)
            s = None
            for i in students:
                if i.name+' '+i.last_name == c:
                    s = Student.objects.filter(name = i.name , last_name = i.last_name).first()
                    break
            

            if not s:
                s = Student.objects.filter(username = c).first()
            context = {'ostad':os,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student3',args = [os.id,s.id]))
            return response
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

class Change2View(generic.TemplateView):#change student's info by admin
    template_name = 'uni/change2.html'
   
   
    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            form = Change2Form(instance=s)
            form.student = s
            # a = Admin.objects.get(pk = admin_id)
            context = {'form':form,'student':s,'admin':a}
            
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            form = Change2Form(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            del form
            
            return HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
            
        elif not form.is_valid():
            s = Student.objects.get(pk = student_id)
            a = Admin2.objects.get(pk = admin_id)
            error_message = f'لطفا فرم را کامل پر کنید'
            context = {'form':form,'student':s,'error_message':error_message,'admin':a}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class ChangePassView3(generic.TemplateView):#change student's password by admin
    template_name = 'uni/changepass3.html'
    
    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            form = ChangePass2()
            context = {'admin':a,'form':form,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,student_id):
        
        a = Admin2.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            form = ChangePass2(request.POST)
            if form.is_valid():
                
                if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                    
                    Student.objects.filter(pk = student_id).update(password = oracle10.hash(form.cleaned_data['pass2'],user=s.username))
                    s = Student.objects.filter(pk = student_id).first()
                    t = Account.objects.filter(username = s.username).first()
                    t.set_password(form.cleaned_data['pass3'])
                    t.save()
                    s.save()
                    global gb
                    gb = 1
                    return HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
                else:
                    error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                    context = {'form':form,'admin':a,'error_message':error_message,'student':s}
                    return render(request,self.template_name,context)
                
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'admin':a,'error_message':error_message,'student':s}
                return render(request,self.template_name,context)   
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    


class StudentsView2(generic.TemplateView):#student list in student
    template_name = 'uni/students2.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        Students = Student.objects.filter(uni = s.uni)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s,'Students':Students}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,student_id):
        Students = Student.objects.all()
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            students = Student.objects.filter(uni = s.uni,College = s.College)
            s2 = None
            for i in students:
                if i.name+' '+i.last_name == c:
                    s2 = Student.objects.filter(name = i.name , last_name = i.last_name).first()
                    break
            

            if not s2:
                s2 = Student.objects.filter(username = c).first()
            context = {'student':s,'Students':Students,'student2':s2}
            response = HttpResponseRedirect(reverse('uni:student2',args = [s.id,s2.id]))
            return response
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))




class Student2View(generic.TemplateView):#studnet profile in student
    template_name = 'uni/student2.html'
    
    def get(self,request,student_id,student2_id):
        s2 = Student.objects.get(pk = student2_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s,'student2':s2}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class ElamView2(generic.TemplateView):
    template_name = 'uni/elam2.html'
    
    def get(self,request,ostad_id,el):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,el):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                timess = request.POST.getlist('timeclass')
                

                te = ''
                for i in timess:
                    te = te + i + ' '
                if te == '':
                    error_message = 'لطفا یک زمان را انتخاب کنید'
                    context = {'ostad':os,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                ellist = el.split('--')

                w = Elam.objects.filter(username = os.username ,ostad = ellist[0],dars = ellist[1],goruh = ellist[2]).first()

                

                w.time = te
                w.time = starfunc(w.time)
                w.public_date = dt.datetime.now()
                w.save()
                message = f'برنامه شما به ادمین دانشکده {w.college} ارسال شد'
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                if w.time == '':
                    w.delete()
                return response
            


        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))




class CreateView2(generic.TemplateView):#create student by admin
    
    template_name = 'uni/create2.html'
    
    
    def get(self,request ,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            form = sabtform2()
            context = {'form':form,'admin':a}
            return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform2(request.POST)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
                
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                
                        error_message = 'لطفا فرم را کامل پر کنید'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request ,self.template_name,context)
                
                date1 = request.POST.get('date')
                form.save()
                user = Account.objects.create_user(username = form.cleaned_data['username'], password=form.cleaned_data['password'])
                user.is_ostad = True
                user.save()
                Ostad.objects.filter(username = z).update(birthday = date1)
                Ostad.objects.filter(username = z).update(login_times = '0')
                Ostad.objects.filter(username = z).update(public_date = dt.datetime.now())
                x = Ostad.objects.filter(username = z).update(password = y)
                form = sabtform()
                message = 'استاد با موفقیت ثبت شد'
                context = {'form':form,'admin':a}
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


        
class ElamView1(generic.TemplateView):
    template_name = 'uni/elam1.html'
    
    
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            
            form = ElamForm(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'ostad_id':os.id})
            context = {'ostad':os,'form':form}
            return render(request,self.template_name,context)
            
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
        

    def post(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            
            form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os,'ostad_id':ostad_id,'phone':os.phone})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    error_message = 'لطفا فرم را کامل پر کنید'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                form.save() 
                ww = list(Elam.objects.filter(dars = form.cleaned_data['dars']).all())
                Elam.objects.filter(username = os.username ,college = form.cleaned_data['college'],dars = form.cleaned_data['dars'],goruh = '').update(goruh = len(ww))
                darsdict = {
                    'فیزیک 1':3,
                    'ریاضی 1':3,
                    'فیزیک 2':3,
                    'ریاضی 2':3,
                    'شیمی':3,
                    'زبان':3,
                    'زبان تخصصی':3,
                    'ادبیات':3,
                    'مبانی کامپیوتر':4,
                    'برنامه نویسی پیشرفته':4,
                    'معادلات دیفرانسیل':3,
                    'ریاضیات گسسته':3,
                    'مدار های الکتریکی و الکترونیکی':3,
                    'مدار منطقی':4,
                    'ساختمان داده':3,
                    'شبکه':3,
                    'جبر خطی کاربردی':3,
                    'آمار احتمال مهندسی':3,
                    'نظریه زبان ها و ماشین ها':3,
                    'معماری کامپیوتر':3,
                    'سیستم عامل':3,
                    'انقلاب':2,
                    'انسان در اسلام':2,
                    'دانش خانواده':2,
                    'تفسیر قرآن':2
                }
                vahed4 = darsdict[form.cleaned_data['dars']]
                w = Elam.objects.filter(username = os.username ,college = form.cleaned_data['college'],dars = form.cleaned_data['dars'],goruh = len(ww)).first()
                w.vahed = vahed4
                w.ostad_id = os.id
                w.vaziat = 'در حال بررسی'
                w.save()

                return HttpResponseRedirect(reverse('uni:elam2',args = [os.id,w]))

            
            
            
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

class BarnameView1(generic.TemplateView):
    template_name = 'uni/barname1.html'
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            e = Elam.objects.filter(uni = a.uni,college = a.College,reject = False,active =False,request = True )
            context = {'admin':a,'Elam':e}
            return render(request,self.template_name,context)
            
            
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
class BarnameView3(generic.TemplateView):
    template_name = 'uni/barname3.html'
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            e = Elam.objects.filter(uni = a.uni,college = a.College,reject = True,active =False ,request = True )
            context = {'admin':a,'Elam':e}
            return render(request,self.template_name,context)
            
            
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class BarnameView2(generic.TemplateView):
    template_name = 'uni/barname2.html'
    
    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            el = Elam.objects.get(pk = elam_id)
            tii = el.time.split(' ')
            tii.sort()
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
            '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
            '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
            '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
            '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            list1 =[]
            for i in tii:
                for j in dictime:
                    if i == j:
                        list1.append(dictime[j])
            context = {'admin':a,'i':el,'lis1':list1}

            return render(request,self.template_name,context)
            
        else:
            logout2(a)

            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        elam = Elam.objects.get(pk = elam_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if request.method == "POST":
                value1 = request.POST.get('dars2')
                if value1 == 'yes':
                    return HttpResponseRedirect(reverse('uni:erae',args = [a.id,elam.id]))
                elif value1 == 'no':
                    elam.reject = True
                    elam.vaziat = 'ارائه نمیشود'
                    elam.save()
                    return HttpResponseRedirect(reverse('uni:barname1',args=[a.id]))

        
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

class BarnameView4(generic.TemplateView):
    template_name = 'uni/barname4.html'
    
    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            el = Elam.objects.get(pk = elam_id)
            tii = el.time.split(' ')
            tii.sort()
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
            '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
            '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
            '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
            '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            list1 =[]
            for i in tii:
                for j in dictime:
                    if i == j:
                        list1.append(dictime[j])
            context = {'admin':a,'i':el,'lis1':list1}

            return render(request,self.template_name,context)
            
        else:
            logout2(a)

            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        elam = Elam.objects.get(pk = elam_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if request.method == "POST":
                value1 = request.POST.get('dars2')
                if value1 == 'yes':
                    return HttpResponseRedirect(reverse('uni:erae',args = [a.id,elam.id]))
                elif value1 == 'no':
                    elam.reject = True
                    elam.save()
                    return HttpResponseRedirect(reverse('uni:barname1',args=[a.id]))

        
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))




class CreateklassView(generic.TemplateView):
    template_name = 'uni/createklass.html'
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        form = KlassForm(initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni})
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            context = {'admin':a,'form':form}
            return render(request,self.template_name,context)
               
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        form = KlassForm(request.POST ,initial = {"college": a.College,'public_date':dt.datetime.now()})
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
                form.save()
                message = 'کلاس با موفقیت ثبت شد'
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))

            
               
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


            



class EraeView(generic.TemplateView):
    template_name = 'uni/erae.html'
    

    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.filter(username = request.user.username).first()
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            elam = Elam.objects.get(pk = elam_id)
            os = Ostad.objects.filter(username = elam.username).first()
            # if uuu == 1:
            #     klaseses = Klass.objects.get(pk = 8)
            #     test(a,elam,klaseses)
            list10 = os.time.split(' ')
            for i in range(len(list10)):
                if list10[i] == '':
                    list10.remove('')
                else:
                    list10[i] = int(list10[i])
            list2 = elam.time.split(' ')
            # list2.pop()
            for i in range(len(list2)):
                if list2[i] == '':
                    list2.remove('')
                else:
                    list2[i] = int(list2[i])
            klas = Klass.objects.filter(college = a.College)
            list3 = []
            
            # u = 0
            # u2 = 0
            for i in klas:
                u = 0
                u2 = 0
                list1 = i.time.split(' ')
                # list1.pop()
                for l in range(len(list1)):
                    
                    if list1[l] == '':
                        list1.remove('')
                    else:
                        list1[l] = int(list1[l])
                for j in list1:
                    if j in list2:
                        u = u + 1
                for j in list2:
                    if j in list10:
                        if j in dic1:
                            if not dic1[j]==i.id:
                                u = u + 1
                if dic1:
                    for h in list(dic1):
                        if dic1[h] == i.id:
                            u2 += 1
                r = len(list2)
                list3.append([i,r - u,u2])
            context = {'klas':list3,'admin':a,'elam':elam}
            return render(request,self.template_name,context)
            
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
dic1 = {}
class Erae2View(generic.TemplateView):
    template_name = 'uni/erae2.html'
    def get(self,request,admin_id,elam_id,klas_id):
        a = Admin2.objects.filter(username = request.user.username).first()
        elam = Elam.objects.get(pk = elam_id)
        klas = Klass.objects.get(pk = klas_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            # if uuu == 1:
            #     test2(a,elam)
            list1 = elam.time.split(' ')
            for i in range(len(list1)):
                if list1[i] == '':
                    list1.remove('')
                else:
                    list1[i] = int(list1[i])
            list2 = klas.time.split(' ')
            for i in range(len(list2)):
                if list2[i] == '':
                    list2.remove('')
                else:
                    list2[i] = int(list2[i])
            
            
           
            
            if elam.active:
                vahed1 = Vahed.objects.filter(elam_id = elam_id).first()
                klases = vahed1.klas_id.split(' ')
                for i in range(len(klases)):
                    if klases[i] == '':
                        klases[i] = None
                # if str(klas_id) in klases:
                    
                list9 = vahed1.time.split(' ')
                list9 = [x for x in list9 if x != '']

                for j in list9:
                    list11 = []
                    list11 = j.split(',')
                    for j in range(len(list11)):
                        if list11[j] == '':
                            list11.remove('')
                        else:
                            list11[j] = int(list11[j])
                        
                        n = list11[0]
                        b = list11[1]
                        dic1[b] = n
                        # os.time += str(n)+' '
                        # os.save()
                        # list10.append(n)

                
                 
                for i in list(dic1):
                    if type(i)==str:
                        dic1.pop(i)
                # else:


            list10 = []
            os = Ostad.objects.filter(username = elam.username).first()
            list10 = os.time.split(' ')
            for i in range(len(list10)):
                if list10[i] == '':
                    list10.remove('')
                else:
                    list10[i] = int(list10[i])

            # for i in list1:
            #     if i in list10:
            #         list1.remove(i)

            # list10.pop()
            # for i in list1:
            #     if i in list2:
            #         list1.remove(i)
            # for i in range(len(list1)):
            #     for j in list10:
            #         if i == j:
            #             del list1[i]
            # zip2 = zip(list1,list10)
            list13= list2 + list10
            list12 = set(list1) - set(list13)
            # list12 = list(set(list1) - set(list10))
            list1 = list(list12)
            
                
            
            # for i in range(len(list1)):
            #     if list1[i] == '01':
            #         list1[i] = 1
            #     if list1[i] == '02':
            #         list1[i] = 2
            #     if list1[i] == '03':
            #         list1[i] = 3
            #     if list1[i] == '04':
            #         list1[i] = 4
            #     if list1[i] == '':
            #         list1[i] = None
            #     else:
            #         list1[i] = int(list1[i])
            # for i in list10:
            #     if i[1] in list1:
            #         list1.remove(i[1])
            # if not elam.active or not klas_id in klases:
            #     # if not klas_id in klases:
            #     list10.append(True)
                    
            # list10.append([1,2])
            list3 = [41,31,21,11,1]
            list4 = [42,32,22,12,2]
            list5 = [43,33,23,13,3]
            list6 = [44,34,24,14,4]
            list7 = [45,35,25,15,5]
            list8 = [0,1,2,3,4]
            # bv = str(type(list10[0]))
            # bv2 = str(type(list1[1]))
            context = {'bv':1,'bv2':1,'list1':list1,'list2':list2,'list3':list3,'admin':a,'list4':list4,'list5':list5,'list6':list6,'list7':list7,'list8':list8,'elam':elam,'klas_id':klas_id,'dic':dic1,'list10':list10}
            return render(request,self.template_name,context)
    def post(self,request,admin_id,elam_id,klas_id):
        cookie  = str(request.COOKIES.get('access'))
        a = Admin2.objects.get(pk = admin_id)
        
        elam = Elam.objects.get(pk = elam_id)
        os = Ostad.objects.filter(username = elam.username).first()
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
                
            if request.method == 'POST':
                
                timess = request.POST.getlist('timeclass')
                timess2 = []
                for i in range(len(timess)):
                    if timess[i] == '':
                        pass
                    else:
                        timess2.append(int(timess[i]))
                vahed1 = Vahed.objects.filter(elam_id = elam_id).first()
                # vahed1.time.replace(f"{klas_id}"," ")
                # vahed1.save()
                for i in list(dic1):
                    if not i in timess2 and dic1[i] == klas_id:
                        
                        kj = vahed1.time
                        kj3 = str(klas_id)+','+str(i)
                        # kj3 = f'{klas_id},{i}'
                        kj2 = kj.replace(kj3,'')
                        vahed1.time = kj2
                        kj = os.time
                        kj2 = kj.replace(f'{i}','')
                        kj2 = re.sub('^\s*','',kj2)
                        os.time = kj2

                        os.save()
                        
                        vahed1.save()
                        dic1.pop(i)
                        klas = Klass.objects.get(pk = klas_id)
                        kj = klas.time

                        kj3 = str(i)
                        kj2 = kj.replace(kj3,'')
                        kj2 = re.sub('^\s*','',kj2)
                        klas.time = kj2
                        kj4 = klas.khali
                        list15 = klas.time.split(' ')
                        if '' in list15:
                            list15.remove('')
                        
                        kj5 = 25 - len(list15)
                        klas.khali = kj5
                        klas.save()

                        # print(dic1[i])
                    
                        
                

                        
                    
                        
                
                klas = Klass.objects.get(pk = klas_id)
                klastimelist = klas.time.split(' ')       
                if '' in klastimelist:
                    klastimelist.remove('')

                if len(timess2) != 0:
                    timee = ''
                    # klas = Klass.objects.get(pk = klas_id)
                    kj = ''
                    for i in timess2:
                        timee += str(klas_id)+',' + str(i) +' '
                        if not str(i) in klastimelist:
                            kj += str(i) + ' '
                            
                            
                    klas.time += kj

                    list15 = klas.time.split(' ')
                    if '' in list15:
                        list15.remove('')
                        
                    kj5 = 25 - len(list15)
                    klas.khali = kj5
                    klas.time = starfunc(klas.time)
                    klas.save() 
                    os.time += kj
                    os.save()      
                    
                    
                    if not elam.active:
                        e = None
                        e = Vahed.objects.filter(elam_id = elam.id).first()
                        # for i in vaheds:
                        #     if i.elam_id == elam.id and i.laghv == True:
                        #         e = i
                        #         e.laghv = False
                        #         break
                        if not e:
                            e = Vahed(time = timee,vahed2 = elam.vahed,sex = elam.sex , uni = elam.uni,ostad = elam.ostad,goruh = elam.goruh , college = elam.college , dars = elam.dars,elam_id = elam_id , capacity = elam.capacity,capacity2 = elam.capacity,ostad_id = elam.ostad_id,por = '0')
                        e.time = timee
                        e.time = starfunc(e.time)
                        e.save()
                        elam.active = True
                        elam.save()

                        
                        c = f'{e.id},'
                        if not  re.search(fr'\b *{c}\b',klas.vaheds) or re.search(fr'\b{c} *\b',klas.vaheds):
                            klas.vaheds += str(e.id) + ' '
                            klas.vaheds = starfunc(klas.vaheds)
                            klas.save()

                        
                        
                        # os.time = timee
                        # os.save()
                    list14 = timee.split(' ')

                    if elam.active:
                        e = Vahed.objects.filter(elam_id = elam_id).first()
                        for i in list14:
                            if not str(i) in e.time:
                                e.time += ' ' + str(i)
                                e.save()
                        os = Ostad.objects.filter(username = elam.username).first()
                        # os.time = timee
                        # os.save()
                    

                    if not str(klas_id) in e.klas_id:
                        e.klas_id += str(klas_id)+ ' '
                        e.klas_id = starfunc(e.klas_id)
                        e.save()


                

                value1 = request.POST.get('erae')

                if value1 == 'back':
                    # uuu = 1
                    return HttpResponseRedirect(reverse('uni:erae' ,args= [a.id,elam.id]))
                if value1 == 'yes':
                    vahed1 = Vahed.objects.filter(elam_id = elam_id).first()
                    return HttpResponseRedirect(reverse('uni:nahaee' ,args= [a.id,elam.id,vahed1.id]))
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
            

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)





class NahaeeView(generic.TemplateView):
    global dic1
    dic1 = {}
    template_name = 'uni/nahaee.html'
    def get(self,request,admin_id,elam_id,vahed_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            elam = Elam.objects.get(pk = elam_id)
            
            vahed1 = Vahed.objects.get(pk = vahed_id)
            os = Ostad.objects.filter(username = elam.username).first()
            kj = str(a.id) + str(elam.goruh) + str(os.id) + str(vahed1.id)
            vahed1.dars_code = kj
            vahed1.save()
            
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            timee = vahed1.time.split(' ')
            for i in timee:
                if i =='':
                    timee.remove(i)
            list3 = []
            for i in timee:
                list2 = i.split(',')
                list3.append(list2[1])
            for i in range(len(list3)):
                if list3[i] == '1':
                    list3[i] = '01'
                if list3[i] == '2':
                    list3[i] = '02'
                if list3[i] == '3':
                    list3[i] = '03'
                if list3[i] == '4':
                    list3[i] = '04'

            list1 =[]
            for i in list3:
                for j in dictime:
                    if i == j:
                        list1.append(dictime[j])    

            context = {'vahed':vahed1,'list1':list1,'admin':a,'elam':elam,'ll':len(list1)}
            
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

        

    def post(self,request,admin_id,elam_id,vahed_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            elam = Elam.objects.get(pk = elam_id)
            elam.vaziat = 'ارارئه میشود'
            elam.accept = True
            elam.reject = False
            elam.save()
            if request.method == "POST":
                vahed1 = Vahed.objects.get(pk = vahed_id)
                value1 = request.POST.get('erae')
                if value1 == 'yes':
                    vahed1.exam = request.POST.get('exam')
                    vahed1.active = True
                    vahed1.laghv = False
                    vahed1.save()
                    message = f'درس {vahed1.dars} با موفقیت ارائه شد'
                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class VahedView(generic.TemplateView):
    template_name = 'uni/vahed.html'
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            vahed1 = Vahed.objects.filter(active = True)
            lastlist = []
            
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3])
                 
            context = {'admin':a,'lastlist':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            vahed__id = request.POST.get('laghv')
            vahed1 = Vahed.objects.get(pk = vahed__id)
            elam1 = Elam.objects.get(pk = vahed1.elam_id)
            os = Ostad.objects.get(pk = vahed1.ostad_id)
            elam1.reject = True
            elam1.accept = False
            elam1.active = False
            elam1.vaziat = 'ارائه نمیشود'
            elam1.save()
            list1 = vahed1.time.split(' ')
            if '' in list1:
                list1.remove('')
            for i in list1:
                list2 = i.split(',')
                klas1 = Klass.objects.get(pk = int(list2[0]))
                
                # klas1.time = klas1.time.replace(list2[1],'')
                c = list2[1]
                if re.search(fr'\b{c} \b',klas1.time) or re.search(fr'\b {c}\b',klas1.time):
                    klas1.khali = str(int(klas1.khali) + 1)
                    klas1.time = re.sub('^\s*','',klas1.time)
                    klas1.time = re.sub(fr'\b {c}\b','',klas1.time)
                    klas1.time = re.sub(fr'\b{c} \b','',klas1.time)
                    klas1.save()
                if re.search(fr'\b{c} \b',os.time) or re.search(fr'\b {c}\b',os.time):
                    os.time = re.sub('^\s*','',os.time)
                    os.time = re.sub(fr'\b {c}\b','',os.time)
                    os.time = re.sub(fr'\b{c} \b','',os.time)
                    os.save()
            vahed1.active = False
            vahed1.accept = False
            vahed1.laghv = True
            vahed1.reject = True
            vahed1.save()
            message = f'درس {vahed1.dars} با موفقیت لغو شد'
            return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
            









class VaziatView(generic.TemplateView):
    template_name = 'uni/vaziat.html'
    def get(self, request, ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            elams = Elam.objects.filter(ostad_id = ostad_id)
            context = {'ostad':os,'elams':elams}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

class Vaziat2View(generic.TemplateView):
    template_name = 'uni/vaziat2.html'
    def get(self, request, ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            elam = Elam.objects.get(pk = elam_id)
            if elam.accept:
                vahed1 = Vahed.objects.filter(elam_id = elam_id).first()
                timee = vahed1.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                dic2 ={}
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                context ={'ostad':os,'dic2':dic2,'vahed':vahed1,'shart':0}
                return render(request,self.template_name,context)
            elif elam.reject:
                context = {'ostad':os,'shart':1,'elam':elam,'elam':elam}
                return render(request,self.template_name,context)
            elif elam.request == False:
                
                list1 =[]
                tii = elam.time.split(' ')
                for i in tii:
                    if i == '':
                        tii.remove(i)
                tii.sort()
                for i in tii:
                    for j in dictime:
                        if i == j:
                            list1.append(dictime[j])
                context = {'elam':elam,'ostad':os,'shart':2,'list1':list1}
                return render(request,self.template_name,context)
            else:
                list1 =[]
                tii = elam.time.split(' ')
                for i in tii:
                    if i == '':
                        tii.remove(i)
                tii.sort()
                for i in tii:
                    for j in dictime:
                        if i == j:
                            list1.append(dictime[j])
                context = {'elam':elam,'ostad':os,'shart':3,'list1':list1}
                return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self, request, ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        elam = Elam.objects.get(pk = elam_id)
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                if request.POST.get('change') == 'vir':
                    response = HttpResponseRedirect(reverse('uni:vaziat3',args = [os.id,elam.id]))
                    return response
                elif request.POST.get('change') == 'cancel':
                    elam.request = False
                    elam.vaziat= 'توسط استاد لغو شده است'
                    elam.save()
                    response = HttpResponseRedirect(reverse('uni:vaziat',args = [os.id]))
                    return response
                
                elif request.POST.get('change') == 'erae':
                    elam.request = True
                    elam.vaziat= 'در حال بررسی'
                    elam.save()
                    response = HttpResponseRedirect(reverse('uni:vaziat',args = [os.id]))
                    return response
                
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))






        

class Vaziat3View(generic.TemplateView):
    template_name = 'uni/vaziat3.html'
    def get(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        elam = Elam.objects.get(pk = elam_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            form = ElamForm(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'college':elam.college,'capacity':elam.capacity,'dars':elam.dars,'sex':elam.sex})
            context = {'ostad':os,'form':form}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            
            form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os,'phone':os.phone})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    error_message = 'لطفا فرم را کامل پر کنید'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                
                
               
                elam = Elam.objects.get(pk = elam_id)
                elam.vaziat = 'در حال بررسی'
                elam.ostad_id = os.id
                elam.college = form.cleaned_data['college']
                elam.uni = form.cleaned_data['uni']
                elam.capacity = form.cleaned_data['capacity']
                elam.save()

                return HttpResponseRedirect(reverse('uni:vaziat4',args = [os.id,elam.id]))
            
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

class Vaziat4View(generic.TemplateView):
    template_name = 'uni/vaziat4.html'
    def get(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                timess = request.POST.getlist('timeclass')
                

                te = ''
                for i in timess:
                    te = te + i + ' '
                if te == '':
                    error_message = 'لطفا یک زمان را انتخاب کنید'
                    context = {'ostad':os,'error_message':error_message}
                    return render(request,self.template_name,context)
                elam = Elam.objects.get(pk = elam_id)
                elam2 = str(elam)
                ellist = elam2.split('--')

                

                

                elam.time = te
                elam.time = starfunc(elam.time)
                elam.public_date = dt.datetime.now()
                elam.save()
                message = 'تغییرات با موفقیت اعمال شد'
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                if elam.time == '':
                    elam.delete()
                return response
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

        

class EntekhabView(generic.TemplateView):
    template_name = 'uni/entekhab.html'
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            # vaheds = Vahed.objects.filter(college = s.College)
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            vahed1 = Vahed.objects.filter(active = True,college = s.College,uni = s.uni)
            lastlist = []
            
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3])
            context = {'student':s,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class Entekhab2View(generic.TemplateView):
    template_name = 'uni/entekhab2.html'
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        

        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            a = Admin2.objects.filter(uni = s.uni,College = s.College).first()
            list2 = a.ejaze.split(' ')
            if '' in list2:
                list2.remove('')
            list3 = []
            for i in list2:
                list3.append(int(i))
            if int(s.enter_year) in list3:
                form = EntekhabForm()
                context = {'student':s,'form':form}
                return render(request,self.template_name,context)
            else:
                message = 'در حال حاضر  مجاز به انتخاب واحد نیستید'
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
            

        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            form = EntekhabForm(request.POST)
            if form.is_valid():

                codedars = form.cleaned_data['codedars']
                goruh = form.cleaned_data['goruh']
                vahed1 = Vahed.objects.filter(dars_code = codedars,uni = s.uni,college = s.College).first()
                if vahed1:
                   
                    return HttpResponseRedirect(reverse('uni:entekhab3',args = [s.id,vahed1.id]))
                elif not vahed1:
                    error_message = 'همچین درسی با این کد و گروه وجود ندارد'
                    context = {'error_message':error_message,'student':s,'form':form}
                    return render(request,self.template_name,context)


            elif not form.is_valid():
                error_message = 'لطفا فرم را کامل پر کنید'
                context = {'error_message':error_message,'student':s,'form':form}
                return render(request,self.template_name,context)
        
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

    

class Entekhab3View(generic.TemplateView):
    template_name = 'uni/entekhab3.html'
    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            
            context = {'vahed':vahed1,'student':s}
            return render(request,self.template_name,context)
        else:   
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            if request.POST.get('entekhab') == 'yes':
                time2 = vahed1.time
                time3 = time2.split(' ')
                time4 = []
                if '' in time3:
                    time3.remove('')
                for i in time3:
                    j = i.split(',')
                    # s.time += j[1]+' '
                    time4.append(j[1])
                if '' in time4:
                    time4.remove('')
                if vahed1.capacity2 == 0:
                    error_message = 'ظرفیت این واحد پر شده است'
                    context = {'vahed':vahed1,'student':s,'error_message':error_message}
                    return render(request,self.template_name,context)

                for i in time4:
                    if re.search(fr'\b{i} *\b',s.time) or re.search(fr'\b *{i}\b',s.time):
                        error_message = 'این واحد با تایم شما منطبق نیست'
                        context = {'vahed':vahed1,'student':s,'error_message':error_message}
                        return render(request,self.template_name,context)

                for i in time4:
                    s.time+= i + ' '

                s.time = starfunc(s.time)
                s.save() 
                vahed1.students += str(s.id) + ' '
                vahed1.capacity2 =  str(int(vahed1.capacity2) - 1)
                vahed1.por = str(int(vahed1.por) + 1)
                vahed1.students = starfunc(vahed1.students)
                vahed1.save()
                s.darses += str(vahed1.id) + ' '
                s.darses = starfunc(s.darses)
                s.save()
                message = f'درس {vahed1.dars} با موفقیت انتخاب شد'
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
            


class MydarsView(generic.TemplateView):
    template_name = 'uni/mydars.html'

    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            # vahed2 = Vahed.objects.filter(active = True,college = s.College,uni = s.uni)
            vahed1 = []
            # c = s.id
            # for i in vahed2:
            #     if re.search(fr'\b *{c}\b',i.students) or re.search(fr'\b{c} *\b',i.students):
            #         vahed1.append(i)
            list6 = s.darses.split(' ')
            if '' in list6:
                list6.remove('')

            for i in list6 :
                if i == '':
                    list6.remove(i)
                    pass
                else:
                    code3 = int(i)
                    vahed3 = Vahed.objects.get(pk = code3)
                    vahed1.append(vahed3)




            lastlist = []
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                try:
                    darkhast1 = Darkhast.objects.filter(student_id = s.id,vahed_id = y.id).first()
                    if darkhast1:
                        darkhast2 = 1
                
                except:
                    darkhast2 = 0
                
                lastlist.append([y,dic2,list4,exam2,exam3,darkhast1])
            
            context = {'student':s,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                vahed_code = int(request.POST.get('laghv'))
                vahed1 = Vahed.objects.get(pk = vahed_code)
                


                return HttpResponseRedirect(reverse('uni:darkhast',args = [s.id,vahed1.id]))
                     
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))


class DarkhastView(generic.TemplateView):
    template_name = 'uni/darkhast.html'
    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            context = {'student':s,'vahed':vahed1}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                if request.POST.get('erae') == 'yes':
                    text2 = request.POST.get('darkhast')
                    e = Darkhast(vahed_id = vahed_id,student_id = s.id,text2 = text2,uni = s.uni,college = s.College )
                    e.save()
                    vahed1 = Vahed.objects.get(pk = vahed_id)
                    message = f'درخواست حذف برای درس {vahed1.dars} به ادمین دانشکده {s.College} ارسال شد'
                    return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))





    
    

class Vahed2View(generic.TemplateView):
    template_name = 'uni/vahed2.html'

    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            s = Student.objects.get(pk = student_id)
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            
            vahed1 = []
            
            list6 = s.darses.split(' ')
            if '' in list6:
                list6.remove('')

            for i in list6 :
                if i == '':
                    list6.remove(i)
                    pass
                else:
                    code3 = int(i)
                    vahed3 = Vahed.objects.get(pk = code3)
                    vahed1.append(vahed3)




            lastlist = []
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3])
            
            context = {'student':s,'admin':a,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class Mydars2View(generic.TemplateView):
    template_name = 'uni/mydars2.html'
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            vahed1 = Vahed.objects.filter(active = True,ostad_id = os.id,laghv = False)
            lastlist = []
            
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3])
                 
            context = {'ostad':os,'lastlist':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
            

class NomreView(generic.TemplateView):
    template_name = 'uni/nomre.html'
    def get(self,request,ostad_id,vahed_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            if vahed1.final:
                final2 = 1
            else:
                final2 = 0
            list3 = vahed1.students.split(' ')
            if '' in list3:
                list3.remove('')
            list4 = []
            for i in list3:
                s = Student.objects.get(pk = int(i))
                c2 = f'{vahed1.id}'
                c4 = re.findall(fr'\b{c2},\d* *\b',s.nomre)
                if not c4:
                    c4 = re.findall(fr'\b *{c2},\d*\b',s.nomre)
                if c4:
                    c5 = c4[0].split(',')
                    list4.append([s,c5[1]])
                elif not c4:
                    list4.append([s,''])
            
            if list4:
                final3 = True
            elif not list4:
                final3 = False
            

            context = {'ostad':os,'students':list4,'nomre':vahed1.nomre2,'final':final2,'final2':final3}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

    def post(self,request,ostad_id,vahed_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            list3 = vahed1.students.split(' ')
            if '' in list3:
                list3.remove('')
            list4 = []
            for i in list3:
                s = Student.objects.get(pk = int(i))
                c2 = f'{vahed1.id}'
                c4 = re.findall(fr'\b{c2},\d* *\b',s.nomre)
                if not c4:
                    c4 = re.findall(fr'\b *{c2},\d*\b',s.nomre)
                if c4:
                    c5 = c4[0].split(',')
                    list4.append([s,c5[1]])
                elif not c4:
                    list4.append([s,''])
            list1 = vahed1.students.split(' ')
            if '' in list1:
                list1.remove('')
            list2 = []
            for i in list1:
                list2.append(Student.objects.get(pk = int(i)))
            nomre_vahed = ''
            if request.method == 'POST':
                for i in list2:
                    nomre1 = request.POST[f"{i.id}"]
                    try:
                        
                        if int(nomre1) > 20 or int(nomre1) < 0:
                            error_message = 'لطفا نمره هارا بین 0 تا 20 وارد کنید.'

                            context = {'ostad':os,'error_message':error_message,'students':list4,'nomre':vahed1.nomre2,'final2':1}

                            return render(request,self.template_name,context)

                        s = Student.objects.get(pk = i.id)
                        c = f'{vahed1.id}'
                        c2 = f'{vahed1.id},{nomre1}'
                        if re.search(fr'\b{c},\d* *\b',s.nomre) or re.search(fr'\b *{c},\d*\b',s.nomre):
                            s.nomre = re.sub(fr'\b{c},\d* *\b',f' {c2} ',s.nomre)
                            s.nomre = re.sub(fr'\b *{c},\d*\b',f' {c2} ',s.nomre)
                        else:
                            s.nomre += ' ' +c2 + ' '
                        
                        c4 = f'{i.id},{nomre1}'
                        s.nomre = starfunc(s.nomre)
                        
                        nomre_vahed += c4+' '
                        s.save()
                        vahed1.save()
                    except ValueError:
                        
                        error_message = 'لطفا نمره هارا فقط با عدد وارد کنید.'

                        context = {'ostad':os,'error_message':error_message,'students':list4,'nomre':vahed1.nomre2,'final2':1}

                        return render(request,self.template_name,context)
                    vahed1.nomre2 = True
                    vahed1.save()
                    if request.POST.get('erae') == 'yes':
                        vahed1.final = True
                        vahed1.save()
                    
                nomre_vahed = starfunc(nomre_vahed)
                vahed1.nomre = nomre_vahed
                vahed1.save()
                message = 'نمرات با موفقیت ثبت شد'
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                return response
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


                    
                    
class KarnameView(generic.TemplateView):
    template_name = 'uni/karname.html'
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            list1 = s.nomre.split(' ')
            av = 0
            final_list = []
            if '' in list1:
                list1.remove('')
            for i in list1:
                list2 = i.split(',')
                if '' in list2:
                    list2.remove('')
                
                vahed1 = Vahed.objects.get(pk = list2[0])
                exam2 = JalaliDateTime(vahed1.exam).strftime("%Y/%m/%d")
                exam3 = JalaliDateTime(vahed1.exam).strftime("%H:%M")
                if float(list2[1]) >= 10:
                    vaziat = 'قبول'
                    color2 = 'green'
                elif float(list2[1]) < 10:
                    vaziat = 'مردود'
                    color2 = 'red'
                if vahed1.final == True:
                    vaziat2 = 'نهایی'
                else:
                    vaziat2 = 'موقت'
                e = Eteraz.objects.filter(uni = s.uni,college = s.College,student_id = s.id,ostad_id = vahed1.ostad_id,vahed_id = vahed1.id).first()
                if e:
                    eter = 1
                elif not e:
                    eter = 0

                final_list.append([vahed1,list2[1],exam2,exam3,vaziat,color2,vaziat2,eter])
            summ = 0
            summ2 = 0
            for i in final_list:
                zarib = int(i[0].vahed2)
                score = int(i[1])
                summ2 += zarib
                summ += zarib*score
            if  not summ2 ==0:
                av = summ / summ2
                if av >= 10:
                    av = float(str(av)[:5])
                elif av < 10:
                    av = float(str(av)[:4])
            else:
                av = 0


                
            context = {'student':s,'vahed_nomre':final_list,'av':av}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))


class Karname2View(generic.TemplateView):
    template_name = 'uni/karname2.html'
    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        s = Student.objects.get(pk = student_id)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            list1 = s.nomre.split(' ')
            av = 0
            final_list = []
            if '' in list1:
                list1.remove('')
            # if not list1:
            #     eror = 'هنوز نمره ای اعلام نشده است'
            #     context = {'student':s,'admin':a,'eror':eror}
            
            #     return render(request,self.template_name,context)

            for i in list1:
                list2 = i.split(',')
                if '' in list2:
                    list2.remove('')
                
                vahed1 = Vahed.objects.get(pk = list2[0])
                exam2 = JalaliDateTime(vahed1.exam).strftime("%Y/%m/%d")
                exam3 = JalaliDateTime(vahed1.exam).strftime("%H:%M")
                if float(list2[1]) >= 10:
                    vaziat = 'قبول'
                    color2 = 'green'
                elif float(list2[1]) < 10:
                    vaziat = 'مردود'
                    color2 = 'red'

                final_list.append([vahed1,list2[1],exam2,exam3,vaziat,color2])
            summ = 0
            summ2 = 0
            for i in final_list:
                zarib = int(i[0].vahed2)
                score = int(i[1])
                summ2 += zarib
                summ += zarib*score
            if final_list:
                av = summ / summ2
                if av >= 10:
                    av = float(str(av)[:5])
                elif av < 10:
                    av = float(str(av)[:4])


                
            context = {'student':s,'vahed_nomre':final_list,'av':av,'admin':a}
            
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
                


class Darkhast2View(generic.TemplateView):
    template_name = 'uni/darkhast2.html'
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            darkhasts = Darkhast.objects.filter(uni = a.uni,college = a.College,accept = False,reject = False)
            lastlist = []
            for i in darkhasts:
                vahed1 = Vahed.objects.get(pk = i.vahed_id)
                s = Student.objects.get(pk = i.student_id)

                lastlist.append([i,s,vahed1])
            context = {'admin':a,'darkhasts':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class Darkhast3View(generic.TemplateView):
    template_name = 'uni/darkhast3.html'
    def get(self,request,admin_id,darkhast_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            darkhast1 = Darkhast.objects.get(pk = darkhast_id)
            s = Student.objects.get(pk = darkhast1.student_id)
            vahed1 = Vahed.objects.get(pk = darkhast1.vahed_id)
            dars = vahed1.dars
            context = {'darkhast':darkhast1,'admin':a,'student':s,'dars':dars}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,darkhast_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            darkhast1 = Darkhast.objects.get(pk = darkhast_id)
            if request.method == 'POST':
                if request.POST.get('darkhast3') == 'yes':
                    darkhast1.accept = True
                    darkhast1.save()
                    s = Student.objects.get(pk = darkhast1.student_id)
                    vahed1 = Vahed.objects.get(pk = darkhast1.vahed_id)
                    vahed1.por = str(int(vahed1.por) - 1)
                    vahed1.capacity2 = str(int(vahed1.capacity2) + 1)
                    
                    c = s.id
                    vahed1.students = re.sub(fr'\b{c} *\b','',vahed1.students)
                    vahed1.students = re.sub(fr'\b *{c}\b','',vahed1.students)
                    vahed1.students = re.sub('^\s*','',vahed1.students)
                    vahed1.students = starfunc(vahed1.students)
                    vahed1.save()
                    c2 = vahed1.id
                    s.darses = re.sub(fr'\b{c2} *\b',' ',s.darses)
                    s.darses = re.sub(fr'\b *{c2}\b',' ',s.darses)
                    s.darses = starfunc(s.darses)
                    s.save()

                    time2 = vahed1.time.split(' ')
                    if '' in time2:
                        time2.remove('')
                    time3 = []
                    for i in time2:
                        j = i.split(',')
                        time3.append(j[1])
                    if '' in time3:
                        time3.remove('')
                    for i in time3:
                        s.time = re.sub(fr'\b{i} *\b','',s.time)
                        s.time = re.sub(fr'\b *{i}\b','',s.time)
                    
                    s.time = starfunc(s.time)
                    s.darses = starfunc(s.darses)
                    c = str(vahed1.id)
                    s.nomre =re.sub(fr'\b{c},\d*',' ',s.nomre)
                    s.nomre = starfunc(s.nomre)
                    s.save()
                    c2 = str(s.id)
                    vahed1.nomre =re.sub(fr'\b{c2},\d*',' ',vahed1.nomre)
                    vahed1.nomre = starfunc(vahed1.nomre)

                    vahed1.save()
                    # if vahed_code:
                    #     raise ValueError
                    message = f'درس {vahed1.dars} برای دانشجو {s.name} {s.last_name} با موفقیت حذف شد'
                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
                elif request.POST.get('darkhast3') == 'no':
                    darkhast1.reject = True
                    darkhast1.save()
                    message = f'درخواست حذف توسط دانشجو {s.name} {s.last_name} با موفقیت رد شد'
                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
                
                
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


        

    
class Darkhast4View(generic.TemplateView):
    template_name = 'uni/darkhast4.html'
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            darkhasts = Darkhast.objects.filter(student_id = s.id)
            lastlist = []
            for i in darkhasts:
                vahed1 = Vahed.objects.get(pk = i.vahed_id)
                if i.accept:
                    vaziat = 'تایید شده است'
                    color2 = 'green'
                elif i.reject:
                    vaziat = 'رد شده است'
                    color2 = 'red'
                else:
                    vaziat = 'در حال بررسی'    
                    color2 = 'black'
                lastlist.append([i,vahed1,vaziat,color2])
            
            context = {'student':s,'darkhasts':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))


class EterazView(generic.TemplateView):
    template_name = 'uni/eteraz.html'
    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:    
            vahed1 = Vahed.objects.get(pk = vahed_id)
            list1 = s.nomre.split(' ')
            if '' in list1:
                list1.remove('')
            for i in list1:
                list2 = i.split(',')
                if '' in list2:
                    list2.remove('')
                if int(list2[0]) == vahed1.id:
                    nomre1 = list2[1]
                    break
            context = {'student':s,'vahed':vahed1,'nomre':nomre1}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            
            if request.method == 'POST':
                
                vahed1 = Vahed.objects.get(pk = vahed_id)
                if request.POST.get('eteraz') == 'yes':
                    
                    e = Eteraz(ostad_id = vahed1.ostad_id,vahed_id = vahed1.id,student_id = s.id,uni = s.uni,college = s.College)
                    e.save()
                    text2 = request.POST.get('darkhast')
                    e.text2 = text2
                    e.save()
                    message = 'اعتراض شما با موفقیت ثبت شد'
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))




class Eteraz2View(generic.TemplateView):
    template_name = 'uni/eteraz2.html'
    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:    
            vahed1 = Vahed.objects.get(pk = vahed_id)
            list1 = s.nomre.split(' ')
            if '' in list1:
                list1.remove('')
            for i in list1:
                list2 = i.split(',')
                if '' in list2:
                    list2.remove('')
                if int(list2[0]) == vahed1.id:
                    nomre1 = list2[1]
                    break
            e = Eteraz.objects.filter(ostad_id = vahed1.ostad_id,vahed_id = vahed1.id,student_id = s.id).first()
            if e.accept == True:
                vaziat = 'تایید شده'
                color2 = 'green'
            elif e.reject == True:
                vaziat = 'رد شده است'
                color2 = 'red'
            else:
                vaziat = 'در حال بررسی'
                color2 = 'black'
            context = {'student':s,'vahed':vahed1,'nomre':nomre1,'eteraz':e,'vaziat':vaziat,'color2':color2}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class Eteraz3View(generic.TemplateView):
    template_name = 'uni/eteraz3.html'
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            e = Eteraz.objects.filter(ostad_id = os.id)
            final_list = []
            for i in e:
                s = Student.objects.get(pk = i.student_id)
                vahed1 = Vahed.objects.get(pk = i.vahed_id)
                list1 = s.nomre.split(' ')
                if '' in list1:
                    list1.remove('')
                for j in list1:
                    list2 = j.split(',')
                    if '' in list2:
                        list2.remove('')
                    if int(list2[0]) == vahed1.id:
                        nomre1 = list2[1]
                        break

                if i.accept == True:
                    vaziat = 'تایید شده'
                    color2 = 'green'
                elif i.reject == True:
                    vaziat = 'رد شده است'
                    color2 = 'red'
                else:
                    vaziat = 'در حال بررسی'
                    color2 = 'black'
                
                final_list.append([s,vahed1,nomre1,vaziat,color2,i])
            context = {'ostad':os,'nomres':final_list}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


class Eteraz4View(generic.TemplateView):
    template_name = 'uni/eteraz4.html'
    def get(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated: 
            e = Eteraz.objects.get(pk = eteraz_id)   
            vahed1 = Vahed.objects.get(pk = e.vahed_id)
            s = Student.objects.get(pk = e.student_id)
            list1 = s.nomre.split(' ')
            if '' in list1:
                list1.remove('')
            for i in list1:
                list2 = i.split(',')
                if '' in list2:
                    list2.remove('')
                if int(list2[0]) == vahed1.id:
                    nomre1 = list2[1]
                    break
            
            if e.accept == True:
                vaziat = 'تایید شده'
                color2 = 'green'
            elif e.reject == True:
                vaziat = 'رد شده است'
                color2 = 'red'
            else:
                vaziat = 'در حال بررسی'
                color2 = 'black'
            context = {'ostad':os,'vahed':vahed1,'nomre':nomre1,'eteraz':e,'vaziat':vaziat,'color2':color2,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))




    def post(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated: 
            e = Eteraz.objects.get(pk = eteraz_id)  
            s = Student.objects.get(pk = e.student_id)
            if request.method == 'POST':
                if request.POST.get('eteraz') == 'yes':
                    if request.POST.get('eteraz2') == 'rad':
                        e.reject = True
                        e.accept = False
                        e.text3 = request.POST.get('javab')
                        e.save()
                        
                        message = f'پاسخ شما برای دانشجو {s.name} {s.last_name} ثبت شد'
                        response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                        return response
                    elif request.POST.get('eteraz2') =='taeed':
                        e.accept = True
                        e.reject = False
                        e.text3 = request.POST.get('javab')
                        e.save()
                        response = HttpResponseRedirect(reverse('uni:eteraz5',args = [os.id,e.id]))
                        return response

                    
                    elif not request.POST.get('eteraz2'):
                        vahed1 = Vahed.objects.get(pk = e.vahed_id)
                        s = Student.objects.get(pk = e.student_id)
                        list1 = s.nomre.split(' ')
                        if '' in list1:
                            list1.remove('')
                        for i in list1:
                            list2 = i.split(',')
                            if '' in list2:
                                list2.remove('')
                            if int(list2[0]) == vahed1.id:
                                nomre1 = list2[1]
                                break
                        
                        if e.accept == True:
                            vaziat = 'تایید شده'
                            color2 = 'green'
                        elif e.reject == True:
                            vaziat = 'رد شده است'
                            color2 = 'red'
                        else:
                            vaziat = 'در حال بررسی'
                            color2 = 'black'
                        error_message = 'لطفااعتراض را رد یا تایید کنید'
                        context = {'ostad':os,'vahed':vahed1,'nomre':nomre1,'eteraz':e,'vaziat':vaziat,'color2':color2,'student':s,'error_message':error_message }
                        return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
                    

                    
class Eteraz5View(generic.TemplateView):
    template_name = 'uni/eteraz5.html'
    def get(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated: 
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            e = Eteraz.objects.get(pk = eteraz_id)  
            vahed1 = Vahed.objects.get(pk = e.vahed_id)
            s = Student.objects.get(pk = e.student_id)
            if request.method == 'POST':
                nomre1 = request.POST.get('new')
                c = str(e.student_id)
                vahed1.nomre = re.sub(fr'\b{c},\d+\b',f' {c},{nomre1} ',vahed1.nomre)
                vahed1.nomre = starfunc(vahed1.nomre)
                vahed1.save()
                c2 = str(vahed1.id)
                s.nomre = re.sub(fr'\b{c2},\d+\b',f' {c2},{nomre1} ',s.nomre)
                s.nomre = starfunc(s.nomre)
                s.save()
                message = f'نمره جدید دانشجو ثبت شد'
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


                

class MessageboxsView(generic.TemplateView):
    template_name = 'uni/messages.html'
    def get(self,request,student_id,message):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class MessageboxaView(generic.TemplateView):
    template_name = 'uni/messagea.html'
    def get(self,request,admin_id,message):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            context = {'admin':a,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

class MessageboxosView(generic.TemplateView):
    template_name = 'uni/messageos.html'
    def get(self,request,ostad_id,message):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))




class MessageboxledView(generic.TemplateView):
    template_name = 'uni/messageled.html'
    def get(self,request,leader_id,message):
        led = Leader.objects.get(pk = leader_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            context = {'leader':led,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))



class MessageboxbsView(generic.TemplateView):
    template_name = 'uni/messagebs.html'
    def get(self,request,boss_id,message):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            context = {'boss':bs,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))





    

class CreatebossView(generic.TemplateView):
    
    template_name = 'uni/createboss.html'
    
    
    def get(self,request ,leader_id):
        led = Leader.objects.get(pk = leader_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            form = sabtform3()
            context = {'form':form,'leader':led}
            return render(request ,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform3(request.POST)
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            if form.is_valid():
                
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                
                        error_message = 'لطفا فرم را کامل پر کنید'
                        context = {'form':form,'leader':led,'error_message':error_message}
                        return render(request ,self.template_name,context)
                
                uni2 = form.cleaned_data['uni']
                if Boss.objects.filter(uni = uni2).first():
                    error_message = 'ادمین دانشگاه وجود دارد'
                    context = {'form':form,'leader':led,'error_message':error_message}
                    return render(request ,self.template_name,context)

                form.save()
                user = Account.objects.create_user(username = form.cleaned_data['username'], password=form.cleaned_data['password'])
                user.is_boss = True
                user.save()
                bs = Boss.objects.filter(username = z).first()
                bs.login_times = '0'
                bs.public_date = dt.datetime.now()
                bs.password = y
               
                bs.save()
                message = 'ادمین با موفقیت ثبت شد'
                return HttpResponseRedirect(reverse('uni:messageled',args = [led.id,message]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'leader':led,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))










class CreateadminView(generic.TemplateView):
    
    template_name = 'uni/createadmin.html'
    
    
    def get(self,request ,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            form = sabtform4()
            context = {'form':form,'boss':bs}
            return render(request ,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform4(request.POST)
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if form.is_valid():
                
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                
                        error_message = 'لطفا فرم را کامل پر کنید'
                        context = {'form':form,'boss':bs,'error_message':error_message}
                        return render(request ,self.template_name,context)
                
                uni2 = bs.uni
                college2 = form.cleaned_data['College']
                if Admin2.objects.filter(uni = uni2,College = college2).first():
                    error_message = 'ادمین دانشکده وجود دارد'
                    context = {'form':form,'boss':bs,'error_message':error_message}
                    return render(request ,self.template_name,context)

                form.save()
                user = Account.objects.create_user(username = form.cleaned_data['username'], password=form.cleaned_data['password'])
                user.is_admin2 = True
                user.save()
                a = Admin2.objects.filter(username = z).first()
                a.login_times = '0'
                a.public_date = dt.datetime.now()
                a.password = y
                a.uni = bs.uni
                a.save()
                message = 'ادمین با موفقیت ثبت شد'
                return HttpResponseRedirect(reverse('uni:messagebs',args = [bs.id,message]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'boss':bs,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))



    
class StudentsbsView(generic.TemplateView):
    template_name = 'uni/studentsbs.html'
    
   
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        Students = Student.objects.filter(uni = bs.uni)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            context = {'boss':bs,'Students':Students}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        Students = Student.objects.filter(uni = bs.uni)
        
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            students = Student.objects.filter(uni = bs.uni)
            s = None
            for i in students:
                if i.name+' '+i.last_name == c:
                    s = Student.objects.filter(name = i.name , last_name = i.last_name).first()
                    break
            

            if not s:
                s = Student.objects.filter(username = c).first()
            context = {'boss':bs,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:studentbs',args = [bs.id,s.id]))
            return response
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




class StudentbsView(generic.TemplateView):
    template_name = 'uni/studentbs.html'
    
    
    def get(self,request,boss_id,student_id):
        s = Student.objects.get(pk = student_id)
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            global gb
            if gb == 1:
                messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                gb = 0
            context = {'boss':bs,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




class AboutSbsView(generic.TemplateView):#student info page in ostad
    
    template_name = 'uni/aboutSbs.html'
    
    def get(self,request,boss_id,student_id):
        
        bs = Boss.objects.get(pk = boss_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            context = {'student':s,'boss':bs}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))







class VahedbsView(generic.TemplateView):
    template_name = 'uni/vahedbs.html'

    def get(self,request,boss_id,student_id):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            s = Student.objects.get(pk = student_id)
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            
            vahed1 = []
            
            list6 = s.darses.split(' ')
            if '' in list6:
                list6.remove('')

            for i in list6 :
                if i == '':
                    list6.remove(i)
                    pass
                else:
                    code3 = int(i)
                    vahed3 = Vahed.objects.get(pk = code3)
                    vahed1.append(vahed3)




            lastlist = []
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3])
            
            context = {'student':s,'boss':bs,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




        







class KarnamebsView(generic.TemplateView):
    template_name = 'uni/karnamebs.html'
    def get(self,request,boss_id,student_id):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))
        s = Student.objects.get(pk = student_id)
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            list1 = s.nomre.split(' ')
            av = 0
            final_list = []
            if '' in list1:
                list1.remove('')
            

            for i in list1:
                list2 = i.split(',')
                if '' in list2:
                    list2.remove('')
                
                vahed1 = Vahed.objects.get(pk = list2[0])
                exam2 = JalaliDateTime(vahed1.exam).strftime("%Y/%m/%d")
                exam3 = JalaliDateTime(vahed1.exam).strftime("%H:%M")
                if float(list2[1]) >= 10:
                    vaziat = 'قبول'
                    color2 = 'green'
                elif float(list2[1]) < 10:
                    vaziat = 'مردود'
                    color2 = 'red'

                final_list.append([vahed1,list2[1],exam2,exam3,vaziat,color2])
            summ = 0
            summ2 = 0
            for i in final_list:
                zarib = int(i[0].vahed2)
                score = int(i[1])
                summ2 += zarib
                summ += zarib*score
            if final_list:
                av = summ / summ2
                if av >= 10:
                    av = float(str(av)[:5])
                elif av < 10:
                    av = float(str(av)[:4])


                
            context = {'student':s,'vahed_nomre':final_list,'av':av,'boss':bs}
            
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




class AdminsbsView(generic.TemplateView):
    template_name = 'uni/adminsbs.html'
    
   
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        admins = Admin2.objects.filter(uni = bs.uni)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            context = {'boss':bs,'admins':admins}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        Students = Student.objects.filter(uni = bs.uni)
        
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            admins = Admin2.objects.filter(uni = bs.uni)
            a = None
            for i in admins:
                if i.name+' '+i.last_name == c:
                    a = Admin2.objects.filter(name = i.name , last_name = i.last_name).first()
                    break
            

            if not a:
                a = Admin2.objects.filter(username = c).first()
            context = {'boss':bs,'admins':admins}
            response = HttpResponseRedirect(reverse('uni:adminbs',args = [bs.id,a.id]))
            return response
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))



class AdminbsView(generic.TemplateView):
    template_name = 'uni/adminbs.html'
    
    
    def get(self,request,boss_id,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            global gb
            if gb == 1:
                messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                gb = 0
            context = {'boss':bs,'admin':a}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))


class Vahedbs2View(generic.TemplateView):
    template_name = 'uni/vahedbs2.html'
    def get(self,request,boss_id,admin_id):
        bs = Boss.objects.get(pk = boss_id)
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            vahed1 = Vahed.objects.filter(active = True,uni = bs.uni,college = a.College)
            lastlist = []
            
            for y in vahed1:
                dic2 = {}
                timee = y.time
                kj = timee.split(' ')
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                list5 = []
                for i in kj:
                    if i =='':
                        kj.remove(i)
                for i in kj:
                    list1.append(i.split(','))
                for i in list1:
                    klas = Klass.objects.get(pk = int(i[0]))
                    list2.append(klas)
                    list3.append(i[1])
                for i in range(len(list3)):
                    if list3[i] == '1':
                        list3[i] = '01'
                    if list3[i] == '2':
                        list3[i] = '02'
                    if list3[i] == '3':
                        list3[i] = '03'
                    if list3[i] == '4':
                        list3[i] = '04'
                for i in list3:
                    for j in dictime:
                        if i == j:
                            list4.append(dictime[j])    
                for i in list2:
                    kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3])
                 
            context = {'admin':a,'lastlist':lastlist,'boss':bs}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))

class EjazeView(generic.TemplateView):
    template_name = 'uni/ejaze.html'
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            a.ejaze = starfunc(a.ejaze)
            a.save()

            list1 = a.ejaze.split(' ')
            if list1:
                if '' in list1:
                    list1.remove('')
                last_list = []
                for i in list1:
                    last_list.append(int(i))
                
            elif not list1:
                last_list = []
            context = {'admin':a,'lastlist':last_list}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                list2 = request.POST.getlist('ejaze')
                str2 = ''
                for i in list2:
                    str2 += ' ' + i +' '
                a.ejaze = str2    
                a.ejaze = starfunc(a.ejaze)
                a.save()
                message = 'دسترسی انتخاب واحد ثبت شد'
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class ChangePassbsView(generic.TemplateView):#change password by student
    template_name = 'uni/changepassbs.html'
    
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            form = ChangePass()
            context = {'boss':bs,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,boss_id):
        
        bs = Boss.objects.get(pk = boss_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            form = ChangePass(request.POST)
            if form.is_valid():
                user = request.user
                if oracle10.hash(form.cleaned_data['pass1'],user = bs.username) == bs.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        bs.password = oracle10.hash(form.cleaned_data['pass3'],user = bs.username)
                        bs.save()
                        user.set_password(form.cleaned_data['pass3'])
                        user.save()
                        global gb
                        gb = 1
                        logout2(bs)
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'boss':bs,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'boss':bs,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'boss':bs,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




class ChangePassledView(generic.TemplateView):#change password by student
    template_name = 'uni/changepassled.html'
    
    def get(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            form = ChangePass()
            context = {'leader':led,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,leader_id):
        
        led = Leader.objects.get(pk = leader_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            form = ChangePass(request.POST)
            if form.is_valid():
                user = request.user
                if oracle10.hash(form.cleaned_data['pass1'],user = led.username) == led.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        led.password = oracle10.hash(form.cleaned_data['pass3'],user = led.username)
                        led.save()
                        user.set_password(form.cleaned_data['pass3'])
                        user.save()
                        global gb
                        gb = 1
                        logout2(led)
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'leader':led,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'leader':led,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'leader':led,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))  
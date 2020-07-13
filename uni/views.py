from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin2, Ostad,Elam,Klass,Account,Vahed
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,sabtform,ChangeForm,ChangePass,Change2Form,ChangePass2,sabtform2,darsform,ElamForm,KlassForm
from django.contrib import messages
from passlib.hash import oracle10
from . import choices
from django import forms
import datetime as dt
from .cookie import CheckCookie,MakeCookie
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.template.defaulttags import register
import re



def page_logout(request):
    if request.method == "POST":
        user = request.user
        if user.is_student:
            s = Student.objects.filter(username = user.username).first()
            s.login_date = None
            s.online = False
            s.save()
        if user.is_admin2:
            a = Admin2.objects.filter(username = user.username)
            a.login_date = None
            a.online = False
        if user.is_ostad:
            o = Ostad.objects.filter(username = user.username)
            o.login_date = None
            o.online = False
            
        logout(request)
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
        

class PageView(generic.TemplateView):#student page
    
    template_name = 'uni/page.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated :
            return render(request,self.template_name,{'student':s})
        
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
    # def post(self,request,ostad_id):
    #     os = Ostad.objects.get(pk = ostad_id)
    #     if CheckCookie(os,request.COOKIES.get('access')):
    #         return render(request,self.template_name,{'ostad':os})
    #     else:
    #         return HttpResponseRedirect(reverse('uni:home'))



class AboutSView(generic.TemplateView):#student info page
    
    template_name = 'uni/aboutS.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s}
            return render(request,self.template_name,context)
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            form = ChangeForm(request.POST,instance=s)
            if form.is_valid():
                form.save()
                
                del form
            
            return HttpResponseRedirect(reverse('uni:page',args = [s.id]))
            
        elif not form.is_valid():
            error_message = f'لطفا فرم را کامل پر کنید'
            context = {'form':form,'student':s,'error_message':error_message}
            return render(request,self.template_name,context)
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        global v
        # v = 0
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform(request.POST)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
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
                success = 'دانشجو با موفقیت ثبت شد'
                context = {'form':form,'admin':a}
                return HttpResponseRedirect(reverse('uni:page2',args = [a.id]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
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
                error_message = "The username or password not currect"
                context = {'form' : form ,'error_message':error_message }
                return render(request ,'uni/login.html',context)
            if user.is_student : 
                s = Student.objects.filter(username = user.username).first()
                response = HttpResponseRedirect(reverse('uni:page',args = [s.id]))
                login(request,user)
                s.login_date = dt.datetime.now()
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
                os.login_times = str(int(os.login_times)+1)
                os.online = True
                os.save()
                h = Ostad.objects.filter(username = form.cleaned_data['username']).first()
                response.set_cookie('access',MakeCookie(h))
                return response  
                      
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
            return HttpResponseRedirect(reverse('uni:home'))


class StudentsView(generic.TemplateView):#student list in admin
    template_name = 'uni/students.html'
    
   
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        Students = Student.objects.filter(College = a.College)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            context = {'admin':a,'Students':Students}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,admin_id):
        Students = Student.objects.all()
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            c2 = c.split(' ')
            last = ''
            for i in range(len(c2)-1):
                if i == len(c2) - 2:
                    last = last + c2[i+1]
                else:
                    last = last + c2[i+1] + ' '
            
            s = Student.objects.filter(name = c2[0] , last_name = last).first()
            

            if not s:
                s = Student.objects.filter(username = c2[0]).first()
            context = {'admin':a,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
            return response
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,ostad_id):
        Students = Student.objects.all()
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            c
            c2 = c.split(' ')
            last = ''
            for i in range(len(c2)-1):
                if i == len(c2) - 2:
                    last = last + c2[i+1]
                else:
                    last = last + c2[i+1] + ' '
            
                
            # if len(c2) == 2:
            s = Student.objects.filter(name = c2[0] , last_name = last).first()
            # if len(c2) == 3:
            #     s2 = Student.objects.filter(name = c2[0] , last_name = c2[1] +' '+ c2[2]).first()

            if not s:
                s = Student.objects.filter(username = c2[0]).first()
            context = {'ostad':os,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student3',args = [os.id,s.id]))
            return response
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,student_id):
        Students = Student.objects.all()
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            c = request.POST.get('search')
            c2 = c.split(' ')
            last = ''
            for i in range(len(c2)-1):
                if i == len(c2) - 2:
                    last = last + c2[i+1]
                else:
                    last = last + c2[i+1] + ' '
            
            s2 = Student.objects.filter(name = c2[0] , last_name = last).first()
            if not s2:
                s2 = Student.objects.filter(username = c2[0]).first()
            context = {'student':s,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student2',args = [s.id,s2.id]))
            return response
        else:
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
                w.public_date = dt.datetime.now()
                w.save()
                response = HttpResponseRedirect(reverse('uni:page3',args = [os.id]))
                if w.time == '':
                    w.delete()
                return response
            


        else:
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
                success = 'استاد با موفقیت ثبت شد'
                context = {'form':form,'admin':a}
                return HttpResponseRedirect(reverse('uni:page2',args = [a.id]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class DarsView(generic.TemplateView):
    template_name = 'uni/dars.html'
    
    
    def get(self,request,ostad_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            form = darsform(instance = os)
            context = {'ostad':os,'form':form}
            return render(request , self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            form = darsform(request.POST)
            if form.is_valid():
                d1 = form.cleaned_data['dars1']
                d2 = form.cleaned_data['dars2']
                d3 = form.cleaned_data['dars3']
                d4 = form.cleaned_data['dars4']
                if d1 == '------------------------------------------------------------------------------':
                    d1 = ''
                if d2 == '------------------------------------------------------------------------------':
                    d2 = ''
                if d3 == '------------------------------------------------------------------------------':
                    d3 = ''
                if d4 == '------------------------------------------------------------------------------':
                    d4 = ''
                
                os.dars1 = d1
                os.dars2 = d2
                os.dars3 = d3
                os.dars4 = d4
                os.save()
              
                
                
                
                
                return HttpResponseRedirect(reverse('uni:page3',args = [os.id]))

        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
        

    def post(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            
            form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    error_message = 'لطفا فرم را کامل پر کنید'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                form.save() 
                ww = list(Elam.objects.filter(dars = form.cleaned_data['dars']).all())
                Elam.objects.filter(username = os.username ,college = form.cleaned_data['college'],dars = form.cleaned_data['dars'],goruh = '').update(goruh = len(ww))
               
                w = Elam.objects.filter(username = os.username ,college = form.cleaned_data['college'],dars = form.cleaned_data['dars'],goruh = len(ww)).first()
                w.vaziat = 'در حال بررسی'
                w.save()

                return HttpResponseRedirect(reverse('uni:elam2',args = [os.id,w]))

            
            
            
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        form = KlassForm(request.POST ,initial = {"college": a.College,'public_date':dt.datetime.now()})
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('uni:page2' ,args= [a.id]))

            
               
        else:
            return HttpResponseRedirect(reverse('uni:home'))


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
                if list10[i] == '01':
                    list10[i] = 1
                if list10[i] == '02':
                    list10[i] = 2
                if list10[i] == '03':
                    list10[i] = 3
                if list10[i] == '04':
                    list10[i] = 4
                if list10[i] == '':
                    list10[i] = None
                else:
                    list10[i] = int(list10[i])
            list2 = elam.time.split(' ')
            # list2.pop()
            for i in range(len(list2)):
                if list2[i] == '01':
                        list2[i] = 1
                if list2[i] == '02':
                    list2[i] = 2
                if list2[i] == '03':
                    list2[i] = 3
                if list2[i] == '04':
                    list2[i] = 4
                if list2[i] == '':
                    list2[i] = None
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
                    if list1[l] == '01':
                        list1[l] = 1
                    if list1[l] == '02':
                        list1[l] = 2
                    if list1[l] == '03':
                        list1[l] = 3
                    if list1[l] == '04':
                        list1[l] = 4
                    if list1[l] == '':
                        list1[l] = None
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
                if list1[i] == '01':
                    list1[i] = 1
                if list1[i] == '02':
                    list1[i] = 2
                if list1[i] == '03':
                    list1[i] = 3
                if list1[i] == '04':
                    list1[i] = 4
                if list1[i] == '':
                    list1[i] = None
                else:
                    list1[i] = int(list1[i])
            list2 = klas.time.split(' ')
            for i in range(len(list2)):
                if list2[i] == '01':
                    list2[i] = 1
                if list2[i] == '02':
                    list2[i] = 2
                if list2[i] == '03':
                    list2[i] = 3
                if list2[i] == '04':
                    list2[i] = 4
                if list2[i] == '':
                    list2[i] = None
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
                        if list11[j] == '01':
                            list11[j] = 1
                        if list11[j] == '02':
                            list11[j] = 2
                        if list11[j] == '03':
                            list11[j] = 3
                        if list11[j] == '04':
                            list11[j] = 4
                        if list11[j] == '':
                            # list11[i] = None
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
                if list10[i] == '01':
                    list10[i] = 1
                if list10[i] == '02':
                    list10[i] = 2
                if list10[i] == '03':
                    list10[i] = 3
                if list10[i] == '04':
                    list10[i] = 4
                if list10[i] == '':
                    list10[i] = None
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
                    if timess[i] == '01':
                        timess2.append(1)
                    if timess[i] == '02':
                        timess2.append(2)
                    if timess[i] == '03':
                        timess2.append(3)
                    if timess[i] == '04':
                        timess2.append(4)
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
                    
                        
                

                        
                    
                        
                
                
                            
                if len(timess2) != 0:
                    timee = ''
                    klas = Klass.objects.get(pk = klas_id)
                    kj = ''
                    for i in timess2:
                        timee += str(klas_id)+',' + str(i) +' '
                        if not str(i) in klas.time:
                            kj += str(i) + ' '
                            
                            
                    klas.time += kj

                    list15 = klas.time.split(' ')
                    if '' in list15:
                        list15.remove('')
                        
                    kj5 = 25 - len(list15)
                    klas.khali = kj5
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
                            e = Vahed(time = timee , uni = elam.uni,ostad = elam.ostad,goruh = elam.goruh , college = elam.college , dars = elam.dars,elam_id = elam_id , capacity = elam.capacity,ostad_id = elam.ostad_id)

                        e.save()
                        elam.active = True
                        elam.save()
                        
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
                        e.save()


                

                value1 = request.POST.get('erae')

                if value1 == 'back':
                    # uuu = 1
                    return HttpResponseRedirect(reverse('uni:erae' ,args= [a.id,elam.id]))
                if value1 == 'yes':
                    vahed1 = Vahed.objects.filter(elam_id = elam_id).first()
                    return HttpResponseRedirect(reverse('uni:nahaee' ,args= [a.id,elam.id,vahed1.id]))
        else:
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
            return HttpResponseRedirect(reverse('uni:home'))

        

    def post(self,request,admin_id,elam_id,vahed_id):
        a = Admin2.objects.get(pk = admin_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            elam = Elam.objects.get(pk = elam_id)
            elam.vaziat = 'ارارعه میشود'
            elam.accept = True
            elam.reject = False
            elam.save()
            if request.method == "POST":
                vahed1 = Vahed.objects.get(pk = vahed_id)
                value1 = request.POST.get('erae')
                date1 = request.POST.get('emtehan')
                if value1 == 'yes':
                    vahed1.active = True
                    vahed1.laghv = False
                    vahed1.emtehan_date = date1
                    vahed1.save()
                    return HttpResponseRedirect(reverse('uni:page2',args = [a.id]))
        else:
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
                    
            
                
                lastlist.append([y,dic2,list4])
                 
            context = {'admin':a,'lastlist':lastlist}
            return render(request,self.template_name,context)
        else:
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
                if list2[1] in klas1.time:
                    klas1.time = klas1.time.replace(list2[1],'')
                    klas1.time = re.sub('^\s*','',klas1.time)

                    klas1.khali = str(int(klas1.khali) + 1)
                    klas1.save()
                if list2[1] in os.time:
                    os.time = os.time.replace(list2[1],'')
                    os.time = re.sub('^\s*','',os.time)
                    os.save()
            vahed1.active = False
            vahed1.accept = False
            vahed1.laghv = True
            vahed1.reject = True
            vahed1.save()
            
            return HttpResponseRedirect(reverse('uni:page2',args = [a.id]))
        else:
            return HttpResponseRedirect(reverse('uni:home'))
            









class VaziatView(generic.TemplateView):
    template_name = 'uni/vaziat.html'
    def get(self, request, ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            ostadname = os.name + ' '+os.last_name
            elams = Elam.objects.filter(ostad = ostadname)
            context = {'ostad':os,'elams':elams}
            return render(request,self.template_name,context)
        else:
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
                # return HttpResponseRedirect(reverse('uni:home'))
                elif request.POST.get('change') == 'erae':
                    elam.request = True
                    elam.vaziat= 'در حال بررسی'
                    elam.save()
                    response = HttpResponseRedirect(reverse('uni:vaziat',args = [os.id]))
                    return response
                
        else:
            return HttpResponseRedirect(reverse('uni:home'))






        

class Vaziat3View(generic.TemplateView):
    template_name = 'uni/vaziat3.html'
    def get(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        elam = Elam.objects.get(pk = elam_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            form = ElamForm(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'college':elam.college,'capacity':elam.capacity,'dars':elam.dars})
            context = {'ostad':os,'form':form}
            return render(request,self.template_name,context)
    def post(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            
            form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    error_message = 'لطفا فرم را کامل پر کنید'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                
                
               
                elam = Elam.objects.get(pk = elam_id)
                elam.vaziat = 'در حال بررسی'
                elam.college = form.cleaned_data['college']
                elam.uni = form.cleaned_data['uni']
                elam.capacity = form.cleaned_data['capacity']
                elam.save()

                return HttpResponseRedirect(reverse('uni:vaziat4',args = [os.id,elam.id]))

class Vaziat4View(generic.TemplateView):
    template_name = 'uni/vaziat4.html'
    def get(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
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
                elam.public_date = dt.datetime.now()
                elam.save()
                response = HttpResponseRedirect(reverse('uni:page3',args = [os.id]))
                if elam.time == '':
                    elam.delete()
                return response
        else:
            return HttpResponseRedirect(reverse('uni:home'))

        

# class Vaziat5View(generic.TemplateView):
#     template_name = 'uni/vaziat.html'
#     def get(self,request,ostad_id,elam_id):
#         elam = Elam.objects.get(pk = elam_id)
#         os = Ostad.objects.get(pk = ostad_id)
#         cookie  = str(request.COOKIES.get('access'))

#         if CheckCookie(os,cookie) and request.user.is_authenticated:
#             elam.request = False
#             elam.save()
#             response = HttpResponseRedirect(reverse('uni:vaziat',args = [os.id]))
#             return response
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))









        










# class VahedView(generic.TemplateView):
#     template_name = 'uni/vahed.html'
#     def get(self,request,admin_id):
#         a = Admin2.objects.get(pk = admin_id)
#         cookie  = str(request.COOKIES.get('access'))
#         if CheckCookie(a,cookie) and request.user.is_authenticated:
#             dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
#                 '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
#                 '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
#                 '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
#                 '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
#             vahed1 = Vahed.objects.filter(active = True)
#             lastlist = []
            
#             for y in vahed1:
#                 dic1 = {}
#                 timee = y.time
#                 kj = timee.split(' ')
#                 list1 = []
#                 list2 = []
#                 list3 = []
#                 list4 = []
#                 list5 = []
#                 for i in kj:
#                     if i =='':
#                         kj.remove(i)
#                 for i in kj:
#                     list1.append(i.split(','))
#                 for i in list1:
#                     klas = Klass.objects.get(pk = int(i[0]))
#                     list2.append(klas)
#                     list3.append(i[1])
#                 for i in range(len(list3)):
#                     if list3[i] == '1':
#                         list3[i] = '01'
#                     if list3[i] == '2':
#                         list3[i] = '02'
#                     if list3[i] == '3':
#                         list3[i] = '03'
#                     if list3[i] == '4':
#                         list3[i] = '04'
#                 for i in list3:
#                     for j in dictime:
#                         if i == j:
#                             list4.append(dictime[j])    
#                 for i in list2:
#                     kj = 'طبقه' +' '+ i.floor +' '+ i.college +' '+ 'کلاس' +' '+ i.number
#                     list5.append(kj)
#                 for i in range(len(list4)):
#                     dic1[list4[i]] = list5[i]
                    
            
                
#                 lastlist.append([y,dic1,list4])
                
            

            
            
            
            

            
                
#             context = {'admin':a,'lastlist':lastlist}
#             return render(request,self.template_name,context)
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))





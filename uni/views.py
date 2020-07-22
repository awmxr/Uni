from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin2, Ostad,Elam,Klass,Account,Vahed,Darkhast,Eteraz,Leader,Boss,Exter,Forget
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,sabtform,ChangeForm,ChangePass,Change2Form,ChangePass2,sabtform2,ElamForm,KlassForm,EntekhabForm,sabtform3,sabtform4
from .forms_en import Loginform_en,sabtform_en,ChangeForm_en,ChangePass_en,Change2Form_en,ChangePass2_en,sabtform2_en,ElamForm_en,KlassForm_en,EntekhabForm_en,sabtform3_en,sabtform4_en
from django.contrib import messages
from passlib.hash import oracle10
from . import choices
from . import choices_en
from .dictt import livedict,religiondict,sexdict,fielddict,collegedict,unidict,gradedict,coursedict,darsdict
from .dictt_en import livedict_en,religiondict_en,sexdict_en,fielddict_en,collegedict_en,unidict_en,gradedict_en,coursedict_en,darsdict_en
from django import forms
import datetime as dt
from .cookie import CheckCookie,MakeCookie,starfunc,manfifunc,replacel,checktime,disapledtime,vahedtime,vahedtime2,replaceii
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.template.defaulttags import register
import re
from persiantools.jdatetime import JalaliDateTime
import socket


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def changetemplate(user,template_name2):
    if user.lang == 'fa':
        template_name = template_name2
    else:
        template_name = re.sub('.html','_en.html',template_name2)
    return template_name


def changelang(user,lang,template_name2):
    user.lang = lang
    aco = Account.objects.filter(username = user.username).first()
    aco.lang = lang
    aco.save()
    user.save()
    if user.lang == 'fa':
        template_name = template_name2
    else:
        template_name = re.sub('.html','_en.html',template_name2)
    return template_name

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
    # template_name_en = 'uni/home_en.html'
    def get(self, request):
        global gb
        if gb == 1:
            messages.success(request, '.پسوورد با موفقیت تغییر کرد لطفا دوباره وارد شوید')
            gb = 0
        return render(request,self.template_name,{'lang':'fa'})
    def post(self, request):
        if request.method == 'POST':
            lang = request.POST.get('lang')
            if lang == 'en':
                return HttpResponseRedirect(reverse('uni:home_en'))
            else:
                return render(request,self.template_name,{'lang':'en'})





    # messages.success(request, 'Password Has Been Changed Successfully Please Login Again')



class Home_enView(generic.TemplateView):
    template_name = 'uni/home_en.html'
    def get(self, request):
        global gb
        if gb == 1:
            messages.success(request, 'Password Has Been Changed Successfully Please Login Again')
            gb = 0
        return render(request,self.template_name,{'lang':'en'})
    def post(self, request):
        if request.method == 'POST':
            lang = request.POST.get('lang')
            if lang == 'fa':
                return HttpResponseRedirect(reverse('uni:home'))
            else:
                return render(request,self.template_name,{'lang':'fa'})



            



class AboutusView(generic.TemplateView):
    template_name = 'uni/aboutus.html'
    # template_name = 'uni/aboutus_en.html'
    def get(self, request,lang):
        if lang == 'fa':
            pass
        else:
            self.template_name = 'uni/aboutus_en.html'

        response = render(request,self.template_name,{})
        return response
        

class PageView(generic.TemplateView):#student page
    
    template_name = 'uni/page.html'
    # template_name = 'uni/page_en.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated :
            return render(request,self.template_name,{'student':s})
        
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated :
            if request.method == 'POST':    
                lang = request.POST.get('lang')
                self.template_name = changelang(s,lang,self.template_name)
                context = {'student':s}
                return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class LeaderView(generic.TemplateView):#student page
    
    template_name = 'uni/leader.html'
    # template_name = 'uni/leader_en.html'

    def get(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        self.template_name = changetemplate(led,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(led,cookie) and request.user.is_authenticated :
            return render(request,self.template_name,{'leader':led})
        
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(led,cookie) and request.user.is_authenticated :
            if request.method == 'POST':    
                lang = request.POST.get('lang')
                self.template_name = changelang(led,lang,self.template_name)
                context = {'leader':led}
                return render(request,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))


class BossView(generic.TemplateView):#student page
    
    template_name = 'uni/boss.html'
    # template_name = 'uni/boss_en.html'

    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated :
            if bs.lang == 'fa':
                uni2 = unidict[bs.uni]
            else:
                uni2 = unidict_en[bs.uni]
            return render(request,self.template_name,{'boss':bs,'uni':uni2})
        
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated :
            if request.method == 'POST':    
                lang = request.POST.get('lang')
                self.template_name = changelang(bs,lang,self.template_name)
                if bs.lang == 'fa':
                    uni2 = unidict[bs.uni]
                else:
                    uni2 = unidict_en[bs.uni]
                context = {'boss':bs,'uni':uni2}
                return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))

            

class Page2View(generic.TemplateView):#admin page
    
    template_name = 'uni/page2.html'
    # template_name = 'uni/page2_en.html'
    
    def get(self,request,admin_id):
        
        # messages.success(request, 'Email sent successfully.')
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        Admins = Admin2.objects.all()
        Students = Student.objects.all()
        cookie  = str(request.COOKIES.get('access'))
        d = CheckCookie(a,cookie)
        if d and request.user.is_authenticated:
            if a.lang == 'fa':
                uni2 = unidict[a.uni]
                college2 = collegedict[a.College]
            else:
                college2 = collegedict_en[a.College]
                uni2 = unidict_en[a.uni]
            return render(request,self.template_name,{'admin':a,'Admins':Admins,'Students':Students,'uni2':uni2,'college2':college2})
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated :
            
            if request.method == 'POST': 
                
                lang = request.POST.get('lang')
                self.template_name = changelang(a,lang,self.template_name)   
                if a.lang == 'fa':
                    uni2 = unidict[a.uni]
                    college2 = collegedict[a.College]
                else:
                    college2 = collegedict_en[a.College]
                    uni2 = unidict_en[a.uni]
                
                context = {'admin':a,'uni2':uni2,'college2':college2}
                return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class Page3View(generic.TemplateView):#ostad page
    
    template_name = 'uni/page3.html'
    # template_name = 'uni/page3_en.html'
    
    def get(self,request,ostad_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        w = Elam.objects.filter(username = os.username ,time = '').first()
        if w and w.time == '':
            w.delete()
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            return render(request,self.template_name,{'ostad':os})
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated :
            if request.method == 'POST':    
                lang = request.POST.get('lang')
                self.template_name = changelang(os,lang,self.template_name)
                context = {'ostad':os}
                return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
  



class AboutSView(generic.TemplateView):#student info page
    
    template_name = 'uni/aboutS.html'
    # template_name = 'uni/aboutS_en.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if s.lang == 'fa':
                field2 = fielddict[s.field]
                college2 = collegedict[s.College]
                uni2 = unidict[s.uni]
            else:
                field2 = fielddict_en[s.field]
                college2 = collegedict_en[s.College]
                uni2 = unidict_en[s.uni]
            context = {'student':s,'field':field2,'college':college2,'uni':uni2}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class AboutS3View(generic.TemplateView):#student info page in ostad
    
    template_name = 'uni/aboutS3.html'
    # template_name = 'uni/aboutS3_en.html'
    
    def get(self,request,ostad_id,student_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                uni2 = unidict[s.uni]
                college2 = collegedict[s.College]
                field2 = fielddict[s.field]
            else:
                uni2 = unidict_en[s.uni]
                college2 = collegedict_en[s.College]
                field2 = fielddict_en[s.field]
            context = {'student':s,'ostad':os,'uni':uni2,'college':college2,'field':field2}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

    
class AboutS2View(generic.TemplateView):#student info page in admin
    
    # template_name = 'uni/aboutS2_en.html'
    template_name = 'uni/aboutS2.html'
    
    def get(self,request,admin_id,student_id):
        
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                uni2 = unidict[s.uni]
                college2 = collegedict[s.College]
                field2 = fielddict[s.field]
            else:
                uni2 = unidict_en[s.uni]
                college2 = collegedict_en[s.College]
                field2 = fielddict_en[s.field]
            context = {'student':s,'admin':a,'uni':uni2,'college':college2,'field':field2}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

    
class ChangeView(generic.TemplateView):#change info by student
    
    # template_name = 'uni/change_en.html'
    template_name = 'uni/change.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if s.lang == 'fa':
                form = ChangeForm(instance=s)
            else:
                form = ChangeForm_en(instance=s)
            form.student = s
            context = {'form':form,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if s.lang == 'fa':
                form = ChangeForm(request.POST,instance=s)
                message = 'تغییرات با موفقیت اعمال شد'
            else:
                form = ChangeForm_en(request.POST,instance=s)
                message = 'Changes Applied Successfully'
            if form.is_valid():
                form.save()
                del form
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
            
            elif not form.is_valid():
                if s.lang == 'fa':
                    error_message = f'لطفا فرم را کامل پر کنید'
                else:
                    error_message = f'Please Complete The Form'
                context = {'form':form,'student':s,'error_message':error_message}
                return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
            



v = 0
class CreateView(generic.TemplateView):#create student by admin
    
    # template_name = 'uni/create_en.html'
    template_name = 'uni/create.html'
    
    def get(self,request ,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = sabtform()
            else:
                form = sabtform_en()
            context = {'form':form,'admin':a}
            return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        global v
        # v = 0
        a = Admin2.objects.get(pk = admin_id)
        
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if a.lang == 'fa':
            form = sabtform(request.POST)
        else:
            form = sabtform_en(request.POST)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
                nam = form.cleaned_data['username']
                users = Account.objects.all()
                for i in users:
                    
                    if i.username == nam:
                        if a.lang == 'fa':
                            error_message = f'این شماره دانشجویی در حال حاضر وجود دارد'
                        else:
                            error_message = f'Student ID Does Not Exist At The Moment'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request ,self.template_name,context)
                

                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                        
                        if a.lang == 'fa':
                            error_message = 'لطفا فرم را کامل پر کنید'
                        else:
                            error_message = 'Please Complete The Form'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request ,self.template_name,context)

                
                date1 = request.POST.get('date')
                form.save()
                Student.objects.filter(username = z).update(birthday = date1)
                Student.objects.filter(username = z).update(login_times = '0')
                Student.objects.filter(username = z).update(public_date = dt.datetime.now())
                user = Account.objects.create_user(username = z,password = form.cleaned_data['password'])
                user.is_student = True
                user.save()
                
                
                
                x = Student.objects.filter(username = z).update(password = y)
                s = Student.objects.filter(username = z).first()
                s.sex = request.POST.get('sex')
                s.save()
                form = sabtform()
                if a.lang == 'fa':
                    message = 'دانشجو با موفقیت ثبت شد'
                else:
                    message = 'Student Added Successfully'
                context = {'form':form,'admin':a}
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
            if form.is_valid() == False:
                if a.lang == 'fa':
                    error_message = f'لطفا فرم را کامل پر کنید'
                else:
                    error_message = f'Please Complete The Form'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
        

        
        
  
class LoginView(generic.TemplateView):#login page
    
    # model = Student
    template_name = 'uni/login.html'
    # template_name = 'uni/login_en.html'

    def get(self , request,lang):
        
        
        
                
        if lang == 'fa':
            form = Loginform()
        else:
            self.template_name = 'uni/login_en.html'
            form = Loginform_en()
        context = {'form' : form,'lang':lang}
        response = render(request,self.template_name,context)
        return response
    

        
    def post(self,request,lang):
        
        if lang == 'fa':
            form = Loginform(request.POST)
        else:
            self.template_name = 'uni/login_en.html'
            form = Loginform_en(request.POST)
        


        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username , password = password)
            if not user:
                
                if lang == 'fa':
                    error_message = "شماره کاربری یا رمز عبور غلط است"
                else:
                    error_message = "Wrong Username or Password !"
            
                context = {'form' : form ,'error_message':error_message }
                return render(request , self.template_name ,context)
            if user.is_student :
                
                s = Student.objects.filter(username = user.username).first()
                aco = Account.objects.filter(username = s.username ).first()
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                aco.ip_address = ip_address
                aco.save()
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
                aco = Account.objects.filter(username = a.username ).first()
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                aco.ip_address = ip_address
                aco.save()
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
                aco = Account.objects.filter(username = os.username ).first()
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                aco.ip_address = ip_address
                aco.save()
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
                aco = Account.objects.filter(username = led.username ).first()
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                aco.ip_address = ip_address
                aco.save()
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
                aco = Account.objects.filter(username = bs.username ).first()
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                aco.ip_address = ip_address
                aco.save()
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

        if lang == 'fa':
            error_message = 'لطفا فرم را کامل پر کنید'
        else:
            error_message = 'Please Complete The Form'
        return render(request,self.template_name,{'form' : form ,'error_message':error_message})

class ChangePassView(generic.TemplateView):#change password by student
    template_name = 'uni/changepass.html'
    # template_name = 'uni/changepass_en.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if s.lang == 'fa':
                form = ChangePass()

            else:
                form = ChangePass_en()
            context = {'student':s,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if s.lang =='fa':
                form = ChangePass(request.POST)
            else:
                form = ChangePass_en(request.POST)
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
                        if s.lang == 'fa':
                            error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        else:
                            error_message = 'New Passwords Must Be Same.'
                        context = {'student':s,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    if s.lang == 'fa':
                        error_message = f'پسوورد قدیمی نادرست است. '
                    else:
                        error_message = f'Your Old Password Is Not True'
                    context = {'student':s,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                if s.lang =='fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'student':s,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))


class ChangePassView2(generic.TemplateView):#change password by admin
    template_name = 'uni/changepass2.html'
    # template_name = 'uni/changepass2_en.html'
    
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            if a.lang == 'fa':
                form = ChangePass()
            else:
                form = ChangePass_en()
            context = {'admin':a,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = ChangePass(request.POST)
            else:
                form = ChangePass_en(request.POST)

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
                        if a.lang == 'fa':
                            error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        else:
                            error_message = 'New Passwords Must Be Same.'
                        context = {'admin':a,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    if a.lang == 'fa':
                        error_message = f'پسوورد قدیمی نادرست است. '
                    else:
                        error_message = f'Your Old Password Is Not True'
                    context = {'admin':a,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                if a.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class ChangePassView4(generic.TemplateView):#change password by ostad
    template_name = 'uni/changepass4.html'
    # template_name = 'uni/changepass4_en.html'
    
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            if os.lang == 'fa':
                form = ChangePass()
            else:
                form = ChangePass_en()
            context = {'ostad':os,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                form = ChangePass(request.POST)
            else:
                form = ChangePass_en(request.POST)
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
                        if os.lang == 'fa':
                            error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        else:
                            error_message = 'New Passwords Must Be Same.'
                        context = {'ostad':os,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    if os.lang == 'fa':
                        error_message = f'پسوورد قدیمی نادرست است. '
                    else:
                        error_message = f'Your Old Password Is Not True'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                if os.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'ostad':os,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


class StudentsView(generic.TemplateView):#student list in admin
    template_name = 'uni/students.html'
    # template_name = 'uni/students_en.html'
    
   
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
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
        self.template_name = changetemplate(a,self.template_name)
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
    # template_name = 'uni/student1_en.html'
    
    
    def get(self,request,admin_id,student_id):
        s = Student.objects.get(pk = student_id)
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            global gb
            if gb == 1:
                if a.lang == 'fa':
                    messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                else:
                    messages.success(request, 'Password Has Been Changed Successfully')
                gb = 0
            context = {'admin':a,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class Student3View(generic.TemplateView):#student profile in ostad
    # template_name = 'uni/student3_en.html'
    template_name = 'uni/student3.html'
    
    def get(self,request,ostad_id,student_id):
        s = Student.objects.get(pk = student_id)
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


    
class Students3View(generic.TemplateView):#student list in ostad
    template_name = 'uni/students3.html'
    # template_name = 'uni/students3_en.html'
    
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
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
        self.template_name = changetemplate(os,self.template_name)
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
    # template_name = 'uni/change2_en.html'
   
   
    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = Change2Form(instance=s)
            else:
                form = Change2Form_en(instance=s)
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
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = Change2Form(request.POST,instance=s)
            else:
                form = Change2Form_en(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            del form
            
            return HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
            
        elif not form.is_valid():
            s = Student.objects.get(pk = student_id)
            a = Admin2.objects.get(pk = admin_id)
            if a.lang == 'fa':
                error_message = f'لطفا فرم را کامل پر کنید'
            else:
                error_message = f'Please Complete The Form'
            
            
            context = {'form':form,'student':s,'error_message':error_message,'admin':a}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class ChangePassView3(generic.TemplateView):#change student's password by admin
    template_name = 'uni/changepass3.html'
    # template_name = 'uni/changepass3_en.html'
    
    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = ChangePass2()
            else:
                form = ChangePass2_en()

            context = {'admin':a,'form':form,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,student_id):
        
        a = Admin2.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = ChangePass2(request.POST)
            else:
                form = ChangePass2_en(request.POST)

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
                    if request.method == 'POST':
                        f2 = request.POST.get('forget')
                        if f2 == '1':
                            f1 = Forget.objects.filter(uni = s.uni,college = s.College,username = s.username,check = False).first()
                            if f1:
                                f1.check = True
                                f1.save()

                    return HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
                else:
                    if a.lang == 'fa':
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                    else:
                        error_message = 'New Passwords Must Be Same.'
                    context = {'form':form,'admin':a,'error_message':error_message,'student':s}
                    return render(request,self.template_name,context)
                
            else:
                if a.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'admin':a,'error_message':error_message,'student':s}
                return render(request,self.template_name,context)   
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    


class StudentsView2(generic.TemplateView):#student list in student
    template_name = 'uni/students2.html'
    # template_name = 'uni/students2_en.html'
    
    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
        self.template_name = changetemplate(s,self.template_name)
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
    # template_name = 'uni/student2_en.html'
    
    def get(self,request,student_id,student2_id):
        s2 = Student.objects.get(pk = student2_id)
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s,'student2':s2}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class ElamView2(generic.TemplateView):
    template_name = 'uni/elam2.html'
    # template_name = 'uni/elam2_en.html'
    
    def get(self,request,ostad_id,el):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,el):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                timess = request.POST.getlist('timeclass')
                

                te = ''
                for i in timess:
                    te = te + i + ' '
                if te == '':
                    if os.lang == 'fa':
                        error_message = 'لطفا یک زمان را انتخاب کنید'
                    else:
                        error_message = 'Please Choose At Least One Time.'
                    context = {'ostad':os,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                ellist = el.split('--')

                w = Elam.objects.filter(username = os.username ,ostad = ellist[0],dars = ellist[1],goruh = ellist[2]).first()

                

                w.time = te
                w.time = starfunc(w.time)
                w.public_date = dt.datetime.now()
                w.save()
                
                if os.lang == 'fa':
                    college2 = collegedict[w.college]
                    message = f'برنامه شما به ادمین دانشکده {college2} ارسال شد'
                else:
                    college2 = collegedict_en[w.college]
                    message = f' Your Schedule Has Been Sent To Admin of {college2} College '
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                if w.time == '':
                    w.delete()
                return response
            


        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))




class CreateView2(generic.TemplateView):#create student by admin
    
    template_name = 'uni/create2.html'
    # template_name = 'uni/create2_en.html'
    
    
    def get(self,request ,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = sabtform2()
            else:
                form = sabtform2_en()
            context = {'form':form,'admin':a}
            return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if a.lang == 'fa':
            form = sabtform2(request.POST)
        else:
            form = sabtform2_en(request.POST)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if form.is_valid():
                
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                ac = Account.objects.all()
                for i in ac:
                    if z == i.username:
                        if a.lang == 'fa':
                            error_message = 'این کد کاربری در حال حاضر موجود میباشد'
                        else:
                            error_message = 'This user code is in use'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request ,self.template_name,context)

                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                        if a.lang == 'fa':
                            error_message = 'لطفا فرم را کامل پر کنید'
                        else:
                            error_message = 'Please Complete The Form'
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
                if a.lang == 'fa':
                    form = sabtform()
                    message = 'استاد با موفقیت ثبت شد'
                else:
                    form = sabtform_en()
                    message = 'Professor Added Successfully'
                context = {'form':form,'admin':a}
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
            if form.is_valid() == False:
                if a.lang == 'fa':
                    error_message = f'لطفا فرم را کامل پر کنید'
                else:
                    error_message = f'Please Complete The Form'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


        
class ElamView1(generic.TemplateView):
    template_name = 'uni/elam1.html'
    # template_name = 'uni/elam1_en.html'
    
    
    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                form = ElamForm(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'ostad_id':os.id})
            else:
                form = ElamForm_en(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'ostad_id':os.id})
            context = {'ostad':os,'form':form}
            return render(request,self.template_name,context)
            
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
        

    def post(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os,'ostad_id':ostad_id,'phone':os.phone})
            else:
                form = ElamForm_en(request.POST,initial = {"username": os.username,'ostad':os,'ostad_id':ostad_id,'phone':os.phone})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    if os.lang == 'fa':
                        error_message = 'لطفا فرم را کامل پر کنید'
                    else:
                        error_message = 'Please Complete The Form'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                form.save() 
                ww = list(Elam.objects.filter(dars = form.cleaned_data['dars']).all())
                Elam.objects.filter(username = os.username ,college = form.cleaned_data['college'],dars = form.cleaned_data['dars'],goruh = '').update(goruh = len(ww))
                
                vaheddict = {
                    '1':3,
                    '2':3,
                    '3':3,
                    '4':3,
                    '5':3,
                    '6':3,
                    '7':3,
                    '8':3,
                    '9':4,
                    '10':4,
                    '11':3,
                    '12':3,
                    '13':3,
                    '14':4,
                    '15':3,
                    '16':3,
                    '17':3,
                    '18':3,
                    '19':3,
                    '20':3,
                    '21':3,
                    '22':2,
                    '23':2,
                    '24':2,
                    '25':2
                }
                vahed4 = vaheddict[form.cleaned_data['dars']]
                w = Elam.objects.filter(username = os.username ,college = form.cleaned_data['college'],dars = form.cleaned_data['dars'],goruh = len(ww)).first()
                w.vahed = vahed4
                w.ostad_id = os.id
                w.vaziat = '0'
                
                w.save()

                return HttpResponseRedirect(reverse('uni:elam2',args = [os.id,w]))

            
            
            
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

class BarnameView1(generic.TemplateView):
    template_name = 'uni/barname1.html'
    # template_name = 'uni/barname1_en.html'
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
            else:
                sexdict = {'1':'female','2':'male','3':'Both'}
            
            e = Elam.objects.filter(uni = a.uni,college = a.College,reject = False,active =False,request = True )
            lastlist = []
            for i in e:
                if a.lang == 'fa':
                    dars2 = darsdict[i.dars]
                else:
                    dars2 = darsdict_en[i.dars]
                lastlist.append([i,sexdict[i.sex],dars2])

            
            context = {'admin':a,'Elam':lastlist}
            return render(request,self.template_name,context)
            
            
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
class BarnameView3(generic.TemplateView):
    template_name = 'uni/barname3.html'
    # template_name = 'uni/barname3_en.html'
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
            else:
                sexdict = {'1':'female','2':'male','3':'Both'}

            e = Elam.objects.filter(uni = a.uni,college = a.College,reject = True,active =False ,request = True )
            lastlist = []
            for i in e:
                if a.lang == 'fa':
                    dars2 = darsdict[i.dars]
                else:
                    dars2 = darsdict_en[i.dars]
                lastlist.append([i,sexdict[i.sex],dars2])
            context = {'admin':a,'Elam':lastlist}
            return render(request,self.template_name,context)
            
            
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class BarnameView2(generic.TemplateView):
    template_name = 'uni/barname2.html'
    # template_name = 'uni/barname2_en.html'
    
    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            el = Elam.objects.get(pk = elam_id)
            tii = el.time.split(' ')
            tii.sort()
            if a.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                dars2 = darsdict[el.dars]
                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                dars2 = darsdict_en[el.dars]
                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
           
            
            list1 =[]
            for i in tii:
                for j in dictime:
                    if i == j:
                        list1.append(dictime[j])
            context = {'admin':a,'i':el,'lis1':list1,'sex':sexdict[el.sex],'dars':dars2}

            return render(request,self.template_name,context)
            
        else:
            logout2(a)

            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        elam = Elam.objects.get(pk = elam_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if request.method == "POST":
                value1 = request.POST.get('dars2')
                if value1 == 'yes':
                    return HttpResponseRedirect(reverse('uni:erae',args = [a.id,elam.id]))
                elif value1 == 'no':
                    elam.reject = True
                    
                    elam.vaziat = '2'
                    elam.save()
                    return HttpResponseRedirect(reverse('uni:barname1',args=[a.id]))

        
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

class BarnameView4(generic.TemplateView):
    template_name = 'uni/barname4.html'
    # template_name = 'uni/barname4_en.html'
    
    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            el = Elam.objects.get(pk = elam_id)
            tii = el.time.split(' ')
            tii.sort()
            if a.lang == 'fa':
                dars2 = darsdict[el.dars]
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                dars2 = darsdict_en[el.dars]
                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
            
            
            list1 =[]
            for i in tii:
                for j in dictime:
                    if i == j:
                        list1.append(dictime[j])
            context = {'admin':a,'i':el,'lis1':list1,'sex':sexdict[el.sex],'dars':dars2}

            return render(request,self.template_name,context)
            
        else:
            logout2(a)

            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
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
    # template_name = 'uni/createklass_en.html'
    
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if a.lang == 'fa':
            form = KlassForm(initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni,'khali':'25'})
        else:
            form = KlassForm_en(initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni,'khali':'25'})
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            context = {'admin':a,'form':form}
            return render(request,self.template_name,context)
               
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang =='fa':
                form = KlassForm(request.POST ,initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni,'khali':'25'})
            else:
                form = KlassForm_en(request.POST ,initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni,'khali':'25'})
            
                
            if form.is_valid():
                
                at = Klass.objects.filter(number = form.cleaned_data['number'] ,college = a.College, uni = a.uni ).first()
                if at:
                    if a.lang == 'fa':
                        form = KlassForm(initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni})
                        error_message = 'این کلاس وجود دارد'
                        
                    else:
                        form = KlassForm_en(initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni})
                        error_message = 'This class already exists'
                    context = {'admin':a,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                else:
                    form.save()
                    if a.lang == 'fa':
                        message = 'کلاس با موفقیت ثبت شد'
                    else:
                        message = 'Class Added Successfully'
                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))

            
               
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


            



class EraeView(generic.TemplateView):
    template_name = 'uni/erae.html'
    # template_name = 'uni/erae_en.html'
    

    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.filter(username = request.user.username).first()
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            elam = Elam.objects.get(pk = elam_id)
            os = Ostad.objects.filter(username = elam.username).first()
            
            list10 = os.time.split(' ')
            for i in range(len(list10)):
                if list10[i] == '':
                    list10.remove('')
                else:
                    list10[i] = int(list10[i])
            list2 = elam.time.split(' ')
            
            for i in range(len(list2)):
                if list2[i] == '':
                    list2.remove('')
                else:
                    list2[i] = int(list2[i])
            klas = Klass.objects.filter(college = a.College)
            list3 = []
            
            
            for i in klas:
                u = 0
                u2 = 0
                list1 = i.time.split(' ')
                
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
    # template_name = 'uni/erae2_en.html'

    def get(self,request,admin_id,elam_id,klas_id):
        a = Admin2.objects.filter(username = request.user.username).first()
        self.template_name = changetemplate(a,self.template_name)
        elam = Elam.objects.get(pk = elam_id)
        klas = Klass.objects.get(pk = klas_id)
        cookie  = str(request.COOKIES.get('access'))
        os = Ostad.objects.get(pk = elam.ostad_id)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
           
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
            
            
           
            checklist = []
            disabeldlist = []
            disabeldlist2 = []
            checklist2 = []
            
            if elam.active:
                exter2 = Exter.objects.filter(elam_id = elam_id).first()
                checklist = checktime(exter2.time_klass,klas_id)
                if ''in checklist:
                    checklist.remove('')
                disabeldlist = disapledtime(exter2.time_klass,klas_id)
                if ''in disabeldlist:
                    disabeldlist.remove('')
                
                for i in range(len(disabeldlist)):
                    disabeldlist2.append(int(disabeldlist[i]))
                for i in range(len(checklist)):
                    checklist2.append(int(checklist[i]))
                
            else:
                elam.active = True
                elam.save()

            list18 = os.time.split(' ')
            if '' in list18:
                list18.remove('')
            
            list13= list(set(list2 + disabeldlist2 ))
            list12 = set(list1) - set(list13)
            list12 = set(list12) - set(checklist2)
            list12 = set(list12) - set(disabeldlist2)
            list1 = list(list12)
            
            
            list3 = [41,31,21,11,1]
            list4 = [42,32,22,12,2]
            list5 = [43,33,23,13,3]
            list6 = [44,34,24,14,4]
            list7 = [45,35,25,15,5]
            list8 = [0,1,2,3,4]

            context = {'bv':list1,'bv2':disabeldlist2,'list1':list1,'list2':list2,'list3':list3,'admin':a,'list4':list4,'list5':list5,'list6':list6,'list7':list7,'list8':list8,'elam':elam,'klas_id':klas_id,'checklist':checklist2}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,elam_id,klas_id):
        cookie  = str(request.COOKIES.get('access'))
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        elam = Elam.objects.get(pk = elam_id)
        os = Ostad.objects.filter(username = elam.username).first()
        klass1 = Klass.objects.get(pk = klas_id)
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            
            if request.method == 'POST':
                timess = request.POST.getlist('timeclass')
                timess2 = []
                for i in range(len(timess)):
                    if timess[i] == '':
                        pass
                    else:
                        timess2.append(int(timess[i]))
                exter_text = ''
                exter2 = Exter.objects.filter(elam_id = elam_id).first()
                if not exter2:
                    exter2 = Exter(elam_id = elam_id)
                for i in timess2:
                    p = str(i)
                    b = re.search(fr'\b{p}\b',exter2.time)
                    if b:
                        exter_text += ' ' + str(i) + ' '
                        pass
                    else:
                        exter_text += ' ' + str(i) + ' '
                        exter2.time += ' ' + str(i) + ' '
                exter2.time = starfunc(exter2.time)
                exter_text = starfunc(exter_text)
                exter_time = exter_text
                
                if exter_text:
                    exter_text = 'i' + exter_text + 'i'
                    exter_text = 'l' + str(klas_id) + ',' + exter_text +'l'
                
                if not exter2:
                    exter2 = Exter(elam_id = elam_id)
                    exter2.save()
                # if exter_text:
                #     exter_time3 = exter_time.split(' ')
                #     if '' in exter_time3:
                #         exter_time3.remove('')
                #     for i in exter_time3:
                #         b = re.search(fr'\b{i}\b',exter_time)
                #         if b:
                #             pass
                #         else:
                #             exter2.time += ' '+i+' '


                exter2.time = starfunc(exter2.time)
                exter2.save()
                if exter_text:
                    exter_text = starfunc(exter_text)
                    b = list(exter_time)
                    b.pop()
                    exter_time = ''
                    for i in b:
                        exter_time+=i
                    
                    # raise ValueError
                    exter2.time_klass = replacel(exter2.time_klass,klas_id,exter_time) 
                    exter2.time_klass = replaceii(exter2.time_klass)
                    exter2.time_klass = manfifunc(exter2.time_klass)
                    exter2.save()
                else:
                    exter2.time_klass = replacel(exter2.time_klass,klas_id,exter_time) 
                    exter2.time_klass = replaceii(exter2.time_klass)
                    exter2.time_klass = manfifunc(exter2.time_klass)
                    exter2.save()


                if request.POST.get('erae') == 'yes':
                   return HttpResponseRedirect(reverse('uni:nahaee',args = [a.id,elam.id])) 

                if request.POST.get('erae') == 'back':
                    return HttpResponseRedirect(reverse('uni:erae',args = [a.id,elam.id]))

                   
                    
                

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
    # template_name = 'uni/nahaee_en.html'
    
    def get(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            elam = Elam.objects.get(pk = elam_id)
            os = Ostad.objects.filter(username = elam.username).first()
            exter2 = Exter.objects.filter(elam_id = elam_id).first()
            kj = str(a.id) + str(elam.goruh) + str(os.id) + str(elam.id)
            exter2.code = kj
            exter2.save()
            # vahed1.dars_code = kj
            
            if a.lang == 'fa':
                dars2 = darsdict[elam.dars]
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                dars2 = darsdict_en[elam.dars]
                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
            
            timee = exter2.time.split(' ')
            for i in timee:
                if i =='':
                    timee.remove(i)
            
            for i in range(len(timee)):
                if timee[i] == '1':
                    timee[i] = '01'
                if timee[i] == '2':
                    timee[i] = '02'
                if timee[i] == '3':
                    timee[i] = '03'
                if timee[i] == '4':
                    timee[i] = '04'

            list1 =[]
            for i in timee:
                for j in dictime:
                    if i == j:
                        list1.append(dictime[j])    

            context = {'list1':list1,'admin':a,'elam':elam,'ll':len(list1),'sex':sexdict[elam.sex],'dars':dars2,'os':os,'exter':exter2}
            
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

        

    def post(self,request,admin_id,elam_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            elam = Elam.objects.get(pk = elam_id)

            
            elam.vaziat = '3'
            
            elam.accept = True
            elam.reject = False
            elam.save()
            if request.method == "POST":
                vahed1 = Vahed.objects.filter(elam_id = elam_id).first()
                value1 = request.POST.get('erae')
                if value1 == 'yes':
                    examdate = request.POST.get('exam')
                    if examdate == '':
                        elam = Elam.objects.get(pk = elam_id)
                        os = Ostad.objects.filter(username = elam.username).first()
                        exter2 = Exter.objects.filter(elam_id = elam_id).first()
                        kj = str(a.id) + str(elam.goruh) + str(os.id) + str(elam.id)
                        exter2.code = kj
                        exter2.save()
                        # vahed1.dars_code = kj
                        
                        if a.lang == 'fa':
                            dars2 = darsdict[elam.dars]
                            sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                            dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                                '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                                '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                                '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                                '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
                        else:
                            dars2 = darsdict_en[elam.dars]
                            sexdict = {'1':'female','2':'male','3':'Both'}
                            dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                            '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                            '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                            '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                            '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
                        
                        timee = exter2.time.split(' ')
                        for i in timee:
                            if i =='':
                                timee.remove(i)
                        
                        for i in range(len(timee)):
                            if timee[i] == '1':
                                timee[i] = '01'
                            if timee[i] == '2':
                                timee[i] = '02'
                            if timee[i] == '3':
                                timee[i] = '03'
                            if timee[i] == '4':
                                timee[i] = '04'

                        list1 =[]
                        for i in timee:
                            for j in dictime:
                                if i == j:
                                    list1.append(dictime[j])    
                        if a.lang == 'fa':
                            error_message = 'لطفا تاریخ را اعلام کنید'
                        else:
                            error_message = 'Please announce the date'

                        context = {'error_message':error_message,'list1':list1,'admin':a,'elam':elam,'ll':len(list1),'sex':sexdict[elam.sex],'dars':dars2,'os':os,'exter':exter2}
                        
                        return render(request,self.template_name,context)

                    elam = Elam.objects.get(pk = elam_id)
                    exter2 = Exter.objects.filter(elam_id = elam_id).first()
                    os = Ostad.objects.filter(username = elam.username).first()
                    exter2.time = starfunc(exter2.time)
                    os.time += ' '+exter2.time+' '
                    os.time = starfunc(os.time)
                    os.save()
                    vahed1 = Vahed.objects.filter(ostad_id = elam.ostad_id,elam_id = elam_id).first()
                    if vahed1:
                        vahed1.time = vahedtime(exter2.time_klass)
                        vahed1.laghv = False
                    elif not vahed1:
                        vahed1 = Vahed(ostad_id = elam.ostad_id,elam_id = elam_id,dars = elam.dars,ostad = elam.ostad,uni = elam.uni,college = elam.college,time = vahedtime(exter2.time_klass),vahed2 = elam.vahed,capacity = elam.capacity,sex = elam.sex,capacity2 = elam.capacity,por = '0',goruh = elam.goruh)
                    vahed1.save()

                    vahed1.time = starfunc(vahed1.time)
                    # kj = str(a.id) + str(elam.goruh) + str(os.id) + str(vahed1.id)
                    # vahed1.dars_code = kj
                    vahed1.save()
                    z3 = vahedtime2(exter2.time_klass)
                    for i in z3:
                        klas3 = Klass.objects.get(pk = int(i[0]))
                        klas3.time += ' ' + i[1] +' '
                        klas3.time = starfunc(klas3.time)
                        klas3.khali = str(int(klas3.khali) - 1)
                        klas3.save()
                    
                    vahed1.exam = request.POST.get('exam')
                    vahed1.active = True
                    vahed1.laghv = False
                    vahed1.save()
                    exter2 = Exter.objects.filter(elam_id = elam_id).first().delete()
                    
                    if a.lang == 'fa':
                        dars2 = darsdict[vahed1.dars]
                        message = f'درس {dars2} با موفقیت ارائه شد'
                    else:
                        dars2 = darsdict_en[vahed1.dars]
                        message = f'The {dars2} Course Has Been Presented Successfully'
                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
                else:
                    exter2 = Exter.objects.filter(elam_id = elam_id).first()
                    if exter2:
                        exter2 = Exter.objects.filter(elam_id = elam_id).first().delete()
                    elam1 = Elam.objects.get(pk = elam_id)
                    elam1.active = False
                    elam1.accept = False
                    # elam1.reject = False
                    elam1.request = True
                    elam1.save()
                    if a.lang == 'fa':
                        message = 'لغو شد'
                    else:
                        
                        message = 'Canceled'
                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))

        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class VahedView(generic.TemplateView):
    template_name = 'uni/vahed.html'
    # template_name = 'uni/vahed_en.html'

    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                
                sexdict = {'1':'female','2':'male','3':'Both'}
                
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
            
            
            
            vahed1 = Vahed.objects.filter(active = True)
            lastlist = []
            
            for y in vahed1:
                dic2 = {}
                if a.lang == 'fa':
                    dars2 = darsdict[y.dars]
                else:
                    dars2 = darsdict_en[y.dars]
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
                    if a.lang == 'fa':
                        college2 = collegedict[i.college]
                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict_en[i.college]
                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3,sexdict[y.sex],dars2])
                 
            context = {'admin':a,'lastlist':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            vahed__id = request.POST.get('laghv')
            vahed1 = Vahed.objects.get(pk = vahed__id)
            elam1 = Elam.objects.get(pk = vahed1.elam_id)
            os = Ostad.objects.get(pk = vahed1.ostad_id)
            elam1.reject = True
            elam1.accept = False
            elam1.active = False
            
            elam1.vaziat = '2'
            elam1.save()
            list1 = vahed1.time.split(' ')
            if '' in list1:
                list1.remove('')
            for i in list1:
                list2 = i.split(',')
                klas1 = Klass.objects.get(pk = int(list2[0]))
                
                
                c = list2[1]
                c = starfunc(c)
                c = c[:-1]
                
                if re.search(fr'\b{c}\b',klas1.time):
                    klas1.khali = str(int(klas1.khali) + 1)
                    klas1.save()
                    klas1.time = starfunc(klas1.time)
                    klas1.time = re.sub(fr'\b{c}\b','',klas1.time)
                    klas1.time = starfunc(klas1.time)
                    klas1.save()
                if re.search(fr'\b{c}\b',os.time):
                    os.time = starfunc(os.time)
                    os.time = re.sub(fr'\b{c}\b','',os.time)
                    os.time = starfunc(os.time)
                    os.save()
            vahed1.active = False
            vahed1.accept = False
            vahed1.laghv = True
            vahed1.reject = True
            vahed1.save()
            if a.lang == 'fa':
                dars2 = darsdict[vahed1.dars]
                message = f'درس {dars2} با موفقیت لغو شد'
            else:
                dars2 = darsdict_en[vahed1.dars]
                message = f'The {dars2} Course Has Been Canceled Successfully'
            
            return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
            









class VaziatView(generic.TemplateView):
    template_name = 'uni/vaziat.html'
    # template_name = 'uni/vaziat_en.html'

    def get(self, request, ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:


            if os.lang == 'fa':
                vaziatdict = {'0':'درحال بررسی','1':'توسط استاد لغو شده','2':'توسط ادمین دانشکده رد شده است','3':'ارائه میشود'}
            else:
                vaziatdict = {'0':'Pending','1':'Canceled By Professor','2':'Not Provided','3':'Presented'}

            
            elams = Elam.objects.filter(ostad_id = ostad_id)
            last_list =[]
            for i in elams:
                if os.lang == 'fa':
                    last_list.append([i,vaziatdict[i.vaziat],darsdict[i.dars],unidict[i.uni],collegedict[i.college]])
                else:
                    last_list.append([i,vaziatdict[i.vaziat],darsdict_en[i.dars],unidict_en[i.uni],collegedict_en[i.college]])
            context = {'ostad':os,'elams':last_list}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

class Vaziat2View(generic.TemplateView):
    template_name = 'uni/vaziat2.html'
    # template_name = 'uni/vaziat2_en.html'

    def get(self, request, ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:        
            
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
            
            
            
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
                    if os.lang == 'fa':
                        college2 = collegedict[i.college]
                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict_en[i.college]
                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                if os.lang == 'fa':
                    context ={'ostad':os,'dic2':dic2,'vahed':vahed1,'shart':0,'dars':darsdict[elam.dars],'uni':unidict[elam.uni],'college':collegedict[elam.college]}
                else:
                    context ={'ostad':os,'dic2':dic2,'vahed':vahed1,'shart':0,'dars':darsdict_en[elam.dars],'uni':unidict_en[elam.uni],'college':collegedict_en[elam.college]}
                return render(request,self.template_name,context)
            elif elam.reject:
                if os.lang == 'fa':
                    context = {'ostad':os,'shart':1,'elam':elam,'elam':elam,'dars':darsdict[elam.dars],'uni':unidict[elam.uni],'college':collegedict[elam.college]}
                else:
                    context = {'ostad':os,'shart':1,'elam':elam,'elam':elam,'dars':darsdict_en[elam.dars],'uni':unidict_en[elam.uni],'college':collegedict_en[elam.college]}
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
                if os.lang == 'fa':
                    context = {'elam':elam,'ostad':os,'shart':2,'list1':list1,'dars':darsdict[elam.dars],'uni':unidict[elam.uni],'college':collegedict[elam.college]}
                else:
                    context = {'elam':elam,'ostad':os,'shart':2,'list1':list1,'dars':darsdict_en[elam.dars],'uni':unidict_en[elam.uni],'college':collegedict_en[elam.college]}
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
                if os.lang == 'fa':
                    context = {'elam':elam,'ostad':os,'shart':3,'list1':list1,'dars':darsdict[elam.dars],'uni':unidict[elam.uni],'college':collegedict[elam.college]}
                else:
                    context = {'elam':elam,'ostad':os,'shart':3,'list1':list1,'dars':darsdict_en[elam.dars],'uni':unidict_en[elam.uni],'college':collegedict_en[elam.college]}
                return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self, request, ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        elam = Elam.objects.get(pk = elam_id)
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                if request.POST.get('change') == 'vir':
                    response = HttpResponseRedirect(reverse('uni:vaziat3',args = [os.id,elam.id]))
                    return response
                elif request.POST.get('change') == 'cancel':
                    elam.request = False
                    elam.vaziat= '1'
                    
                    elam.save()
                    response = HttpResponseRedirect(reverse('uni:vaziat',args = [os.id]))
                    return response
                
                elif request.POST.get('change') == 'erae':
                    elam.request = True
                    
                    elam.vaziat= '0'
                    elam.save()
                    response = HttpResponseRedirect(reverse('uni:vaziat',args = [os.id]))
                    return response
                
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))






        

class Vaziat3View(generic.TemplateView):
    template_name = 'uni/vaziat3.html'
    # template_name = 'uni/vaziat3_en.html'

    def get(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        elam = Elam.objects.get(pk = elam_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                form = ElamForm(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'college':elam.college,'capacity':elam.capacity,'dars':elam.dars,'sex':elam.sex})
            else:
                form = ElamForm_en(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni,'college':elam.college,'capacity':elam.capacity,'dars':elam.dars,'sex':elam.sex})
            context = {'ostad':os,'form':form}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if os.lang == 'fa':
                form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os,'phone':os.phone})
            else:
                form = ElamForm_en(request.POST,initial = {"username": os.username,'ostad':os,'phone':os.phone})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    if os.lang == 'fa':
                        error_message = 'لطفا فرم را کامل پر کنید'
                    else:
                        error_message = 'Please Complete The Form'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                
                
                
               
                elam = Elam.objects.get(pk = elam_id)
                
                elam.vaziat = '0'
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
    # template_name = 'uni/vaziat4_en.html'

    def get(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,elam_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:
            if request.method == 'POST':
                timess = request.POST.getlist('timeclass')
                

                te = ''
                for i in timess:
                    te = te + i + ' '
                if te == '':
                    if os.lang == 'fa':
                        error_message = 'لطفا یک زمان را انتخاب کنید'
                    else:
                        error_message = 'Please Choose At Least One Time'
                    context = {'ostad':os,'error_message':error_message}
                    return render(request,self.template_name,context)
                elam = Elam.objects.get(pk = elam_id)
                elam2 = str(elam)
                ellist = elam2.split('--')

                

                

                elam.time = te
                elam.time = starfunc(elam.time)
                elam.public_date = dt.datetime.now()
                elam.save()
                if os.lang == 'fa':
                    message = 'تغییرات با موفقیت اعمال شد'
                else:
                    message = 'Changes Applied Successfully'
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                if elam.time == '':
                    elam.delete()
                return response
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))

        

class EntekhabView(generic.TemplateView):
    template_name = 'uni/entekhab.html'
    # template_name = 'uni/entekhab_en.html'

    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            # vaheds = Vahed.objects.filter(college = s.College)
            if s.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}

                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                
                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
            
            
            
            vahed1 = Vahed.objects.filter(active = True,college = s.College,uni = s.uni)
            lastlist = []
            
            for y in vahed1:
                if s.lang == 'fa':
                    dars2 = darsdict[y.dars]
                else:
                    dars2 = darsdict_en[y.dars]
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
                    if s.lang == 'fa':
                        college2 = collegedict[i.college]
                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict_en[i.college]
                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3,sexdict[y.sex],dars2])
            context = {'student':s,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class Entekhab2View(generic.TemplateView):
    template_name = 'uni/entekhab2.html'
    # template_name = 'uni/entekhab2_en.html'

    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        

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
                if s.lang == 'fa':
                    form = EntekhabForm()
                else:
                    form = EntekhabForm_en()
                context = {'student':s,'form':form}
                return render(request,self.template_name,context)
            else:
                if s.lang == 'fa':
                    message = 'در حال حاضر  مجاز به انتخاب واحد نیستید'
                else:
                    message = 'You Are Not Allowed To Select Any Unit At The Moment'
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
            

        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
                    if s.lang == 'fa':
                        error_message = 'چنین درسی با این کد و گروه وجود ندارد'
                    else:
                        error_message = 'No Course Available By This Course Code & Course Group !'
                    context = {'error_message':error_message,'student':s,'form':form}
                    return render(request,self.template_name,context)


            elif not form.is_valid():
                if s.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید'
                else:
                    error_message = 'Please Complete The Form'
                context = {'error_message':error_message,'student':s,'form':form}
                return render(request,self.template_name,context)
        
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

    

class Entekhab3View(generic.TemplateView):
    template_name = 'uni/entekhab3.html'
    # template_name = 'uni/entekhab3_en.html'

    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            if s.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                dars2 = darsdict[vahed1.dars]
            else:
                sexdict = {'1':'female','2':'male','3':'Both'}
                dars2 = darsdict_en[vahed1.dars]

            context = {'vahed':vahed1,'student':s,'sex':sexdict[vahed1.sex],'dars':dars2}
            return render(request,self.template_name,context)
        else:   
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            if request.POST.get('entekhab') == 'yes':
                if vahed1.sex == '3' or vahed1.sex == s.sex:
                    
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
                        if s.lang == 'fa':
                            dars2 = darsdict[vahed1.dars]
                            error_message = 'ظرفیت این واحد پر شده است'
                        else:
                            dars2 = darsdict_en[vahed1.dars]
                            error_message = 'Capacity Is Completed !'

                        context = {'vahed':vahed1,'student':s,'error_message':error_message,'sex':sexdict[vahed1.sex],'dars':dars2}
                        return render(request,self.template_name,context)

                    for i in time4:
                        if re.search(fr'\b{i} *\b',s.time) or re.search(fr'\b *{i}\b',s.time):
                            if s.lang == 'fa':
                                dars2 = darsdict[vahed1.dars]
                                error_message = 'این واحد با تایم شما منطبق نیست'
                            else:
                                dars2 = darsdict_en[vahed1.dars]
                                error_message = 'This Course Is Not Available For You'

                            context = {'vahed':vahed1,'student':s,'error_message':error_message,'sex':sexdict[vahed1.sex],'dars':dars2}
                            return render(request,self.template_name,context)
                    s.time = starfunc(s.time)
                    for i in time4:
                        s.time+= i + ' '

                    s.time = starfunc(s.time)
                    s.save() 
                    vahed1.students += str(s.id) + ' '
                    vahed1.capacity2 =  str(int(vahed1.capacity2) - 1)
                    vahed1.por = str(int(vahed1.por) + 1)
                    vahed1.students = starfunc(vahed1.students)
                    vahed1.save()
                    s.darses = starfunc(s.darses)
                    s.darses += str(vahed1.id) + ' '
                    s.darses = starfunc(s.darses)
                    s.save()
                    

                    if s.lang == 'fa':
                        dars2 = darsdict[vahed1.dars]
                        message = f'درس {dars2} با موفقیت انتخاب شد'
                    else:
                        dars2 = darsdict_en[dars]
                        message = f'{dars2} Course Has Been Selected Successfully'
                    return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
                elif not s.sex == vahed1.sex:
                    if s.lang == 'fa':
                        error_message = 'این واحد برای شما قابل ارائه نیست'
                    else:
                        error_message = 'This Course Is Not Available For You'

                    context = {'vahed':vahed1,'student':s,'error_message':error_message}
                    return render(request,self.template_name,context)

                    
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
            


class MydarsView(generic.TemplateView):
    template_name = 'uni/mydars.html'
    # template_name = 'uni/mydars_en.html'

    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            if s.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}
                
                

                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:        
                
                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
       
            
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
                if s.lang == 'fa':
                    dars2 = darsdict[y.dars]
                else:
                    dars2 = darsdict_en[y.dars]
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
                    if s.lang == 'fa':
                        college2 = collegedict[i.college]
                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict_en[i.college]
                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
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
                
                lastlist.append([y,dic2,list4,exam2,exam3,darkhast1,sexdict[y.sex],dars2])
            
            context = {'student':s,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

    def post(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
    # template_name = 'uni/darkhast_en.html'


    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            vahed1 = Vahed.objects.get(pk = vahed_id)
            if request.method == 'POST':
                if request.POST.get('erae') == 'yes':
                    text2 = request.POST.get('darkhast')
                    e = Darkhast(vahed_id = vahed_id,student_id = s.id,text2 = text2,uni = s.uni,college = s.College )
                    e.save()
                    vahed1 = Vahed.objects.get(pk = vahed_id)
                    if s.lang == 'fa':
                        dars2 = darsdict[vahed1.dars]
                        college2 = collegedict[s.College]
                        message = f'درخواست حذف برای درس {dars2} به ادمین دانشکده {college2} ارسال شد'
                    else:
                        dars2 = darsdict_en[vahed1.dars]
                        college2 = collegedict_en[s.College]

                        message = f'Request For Deleting {dars2} Course Has Been Sent to {college2} College Admin'
                    return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))





    
    

class Vahed2View(generic.TemplateView):
    template_name = 'uni/vahed2.html'
    # template_name = 'uni/vahed2_en.html'

    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie) and request.user.is_authenticated:
            s = Student.objects.get(pk = student_id)
            if a.lang == 'fa':

                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
            
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
       


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
                if a.lang == 'fa':
                    sex = sexdict[y.sex]
                    dars2 = darsdict[y.dars]
                else:
                    sex = sexdict_en[y.sex]
                    dars2 = darsdict_en[y.dars]
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
                    if a.lang == 'fa':
                        
                        college2 = collegedict[i.college]

                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        
                        college2 = collegedict_en[i.college]

                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                
                lastlist.append([y,dic2,list4,exam2,exam3,dars2,sex])
            
            context = {'student':s,'admin':a,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class Mydars2View(generic.TemplateView):
    template_name = 'uni/mydars2.html'
    # template_name = 'uni/mydars2_en.html'

    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie) and request.user.is_authenticated:

            if os.lang == 'fa':
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}

                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                
                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
       
            
            vahed1 = Vahed.objects.filter(active = True,ostad_id = os.id,laghv = False)
            lastlist = []
            
            for y in vahed1:
                if os.lang == 'fa':
                    dars2 = darsdict[y.dars]
                else:
                    dars2 = darsdict_en[y.dars]
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
                    if os.lang == 'fa':
                        college2 = collegedict[i.college]

                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict_en[i.college]

                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                sex2 = sexdict[y.sex]
                lastlist.append([y,dic2,list4,exam2,exam3,sex2,dars2])
                 
            context = {'ostad':os,'lastlist':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
            

class NomreView(generic.TemplateView):
    template_name = 'uni/nomre.html'
    # template_name = 'uni/nomre_en.html'

    def get(self,request,ostad_id,vahed_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
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
        self.template_name = changetemplate(os,self.template_name)
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
                            if os.lang == 'fa':
                                error_message = 'لطفا نمره هارا بین 0 تا 20 وارد کنید.'
                            else:
                                error_message = 'Please Enter The Score Between 0 & 20'

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
                        if os.lang == 'fa':
                            error_message = 'لطفا نمره هارا فقط با عدد وارد کنید.'
                        else:
                            error_message = 'The Score Must Be Integer'

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
                if os.lang == 'fa':
                    message = 'نمرات با موفقیت ثبت شد'
                else:
                    message = 'Scores Has Been Confirmed Successfully'
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                return response
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


                    
                    
class KarnameView(generic.TemplateView):
    template_name = 'uni/karname.html'
    # template_name = 'uni/karname_en.html'

    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
                    if s.lang == 'fa':
                        vaziat = 'قبول'
                    else:
                        vaziat = 'Accepted'
                    color2 = 'green'
                elif float(list2[1]) < 10:
                    if s.lang == 'fa':
                        vaziat = 'مردود'
                    else:
                        vaziat = 'Rejected'
                    color2 = 'red'
                if vahed1.final == True:
                    if s.lang == 'fa':
                        vaziat2 = 'نهایی'
                    else:
                        vaziat2 = 'Final'
                else:
                    if s.lang == 'fa':
                        vaziat2 = 'موقت'
                    else:
                        vaziat2 = 'Temporary'
                e = Eteraz.objects.filter(uni = s.uni,college = s.College,student_id = s.id,ostad_id = vahed1.ostad_id,vahed_id = vahed1.id).first()
                if e:
                    eter = 1
                elif not e:
                    eter = 0
                if s.lang == 'fa':
                    dars2 = darsdict[vahed1.dars]
                else:
                    dars2 = darsdict_en[vahed1.dars]
                final_list.append([vahed1,list2[1],exam2,exam3,vaziat,color2,vaziat2,eter,dars2])
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
    # template_name = 'uni/karname2_en.html'

    def get(self,request,admin_id,student_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
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
                    if a.lang == 'fa':
                        vaziat = 'قبول'
                    else:
                        vaziat = 'Accepted'
                    color2 = 'green'
                elif float(list2[1]) < 10:
                    if a.lang == 'fa':
                        vaziat = 'مردود'
                    else:
                        vaziat = 'Rejected'
                    color2 = 'red'
                if a.lang == 'fa':
                    dars2 = darsdict[vahed1.dars]
                else:
                    dars2 = darsdict_en[vahed1.dars]
                final_list.append([vahed1,list2[1],exam2,exam3,vaziat,color2,dars2])
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
    # template_name = 'uni/darkhast2_en.html'

    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            darkhasts = Darkhast.objects.filter(uni = a.uni,college = a.College,accept = False,reject = False)
            lastlist = []
            for i in darkhasts:
                vahed1 = Vahed.objects.get(pk = i.vahed_id)
                s = Student.objects.get(pk = i.student_id)
                if a.lang == 'fa':
                    dars2 = darsdict[vahed1.dars]
                else:
                    dars2 = darsdict_en[vahed1.dars]
                lastlist.append([i,s,vahed1,dars2])
            context = {'admin':a,'darkhasts':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


class Darkhast3View(generic.TemplateView):
    template_name = 'uni/darkhast3.html'
    # template_name = 'uni/darkhast3_en.html'

    def get(self,request,admin_id,darkhast_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            darkhast1 = Darkhast.objects.get(pk = darkhast_id)
            s = Student.objects.get(pk = darkhast1.student_id)
            vahed1 = Vahed.objects.get(pk = darkhast1.vahed_id)
            if s.lang == 'fa':
                dars = darsdict[vahed1.dars]
            else:
                dars = darsdict_en[vahed1.dars]
            context = {'darkhast':darkhast1,'admin':a,'student':s,'dars':dars}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,darkhast_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
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
                        s.time = starfunc(s.time)
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
                    if a.lang == 'fa':
                        message = f'درس {vahed1.dars} برای دانشجو {s.name} {s.last_name} با موفقیت حذف شد'
                    else:
                        message = f'Course {vahed1.dars} Has Been Deleted Successfully For {s.name} {s.last_name}'

                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
                elif request.POST.get('darkhast3') == 'no':
                    s = Student.objects.get(pk = darkhast1.student_id)
                    darkhast1.reject = True
                    darkhast1.save()
                    if a.lang == 'fa':
                        message = f'درخواست حذف توسط دانشجو {s.name} {s.last_name} با موفقیت رد شد'
                    else:
                        message = f'Request of Deleting By {s.name} {s.last_name} Has Been Rejected Successfully'

                    return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
                
                
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))


        

    
class Darkhast4View(generic.TemplateView):
    template_name = 'uni/darkhast4.html'
    # template_name = 'uni/darkhast4_en.html'

    def get(self,request,student_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            darkhasts = Darkhast.objects.filter(student_id = s.id)
            lastlist = []
            for i in darkhasts:
                vahed1 = Vahed.objects.get(pk = i.vahed_id)
                if i.accept:
                    if s.lang == 'fa':
                        vaziat = 'تایید شده است'
                    else:
                        vaziat = 'Has Been Accepted'
                    color2 = 'green'
                elif i.reject:
                    if s.lang == 'fa':
                        vaziat = 'رد شده است'
                    else:
                        vaziat = 'Has Been Rejected'
                    color2 = 'red'
                else:
                    if s.lang == 'fa':
                        vaziat = 'در حال بررسی'    
                    else:
                        vaziat = 'Pending'  
                    color2 = 'black'
                if s.lang == 'fa':
                    dars2 = darsdict[vahed1.dars]
                else:
                    dars2 = darsdict_en[vahed1.dars]
                lastlist.append([i,vahed1,vaziat,color2,dars2])
            
            context = {'student':s,'darkhasts':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))


class EterazView(generic.TemplateView):
    template_name = 'uni/eteraz.html'
    # template_name = 'uni/eteraz_en.html'

    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
            if s.lang == 'fa':
                dars2 = darsdict[vahed1.dars]
            else:
                dars2 = darsdict_en[vahed1.dars]

            
            context = {'student':s,'vahed':vahed1,'nomre':nomre1,'dars':dars2}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
                    if s.lang == 'fa':
                        message = 'اعتراض شما با موفقیت ثبت شد'
                    else:
                        message = 'Your Protest Has Been Confirmed Successfully'
                return HttpResponseRedirect(reverse('uni:messages',args = [s.id,message]))
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))




class Eteraz2View(generic.TemplateView):
    template_name = 'uni/eteraz2.html'
    # template_name = 'uni/eteraz2_en.html'

    def get(self,request,student_id,vahed_id):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
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
                if s.lang == 'fa':
                    vaziat = 'تایید شده'
                else:
                    vaziat = 'Has Been Accepted'
                color2 = 'green'
            elif e.reject == True:
                if s.lang == 'fa':
                    vaziat = 'رد شده است'
                else:
                    vaziat = 'Has Been Rejected'
                color2 = 'red'
            else:
                if s.lang == 'fa':
                    vaziat = 'در حال بررسی'
                else:
                    vaziat = 'Pending'
                color2 = 'black'
            context = {'student':s,'vahed':vahed1,'nomre':nomre1,'eteraz':e,'vaziat':vaziat,'color2':color2}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class Eteraz3View(generic.TemplateView):
    template_name = 'uni/eteraz3.html'
    # template_name = 'uni/eteraz3_en.html'

    def get(self,request,ostad_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
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
                    if os.lang == 'fa':
                        vaziat = 'تایید شده'
                    else:
                        vaziat = 'Has Been Accepted'
                    color2 = 'green'
                elif i.reject == True:
                    if os.lang == 'fa':
                        vaziat = 'رد شده است'
                    else:
                        vaziat = 'Has Been Rejected'
                    color2 = 'red'
                else:
                    if os.lang == 'fa':
                        vaziat = 'در حال بررسی'
                    else:
                        vaziat = 'Pending'
                    color2 = 'black'
                if os.lang == 'fa':
                    dars2 = darsdict[vahed1.dars]
                else :
                    dars2 = darsdict_en[vahed1.dars]
                final_list.append([s,vahed1,nomre1,vaziat,color2,i,dars2])
            context = {'ostad':os,'nomres':final_list}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


class Eteraz4View(generic.TemplateView):
    template_name = 'uni/eteraz4.html'
    # template_name = 'uni/eteraz4_en.html'

    def get(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
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
                if os.lang == 'fa':
                    vaziat = 'تایید شده'
                else:
                    vaziat = 'Has Been Accepted'
                color2 = 'green'
            elif e.reject == True:
                if os.lang == 'fa':
                    vaziat = 'رد شده است'
                else:
                    vaziat = 'Has Been Rejected'
                color2 = 'red'
            else:
                if os.lang == 'fa':
                    vaziat = 'در حال بررسی'
                else:
                    vaziat = 'Pending'
                color2 = 'black'
            if os.lang == 'fa':
                dars2 = darsdict[vahed1.dars]
            else:
                dars2 = darsdict_en[vahed1.dars]
            context = {'ostad':os,'vahed':vahed1,'nomre':nomre1,'eteraz':e,'vaziat':vaziat,'color2':color2,'student':s,'dars':dars2}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))




    def post(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
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
                        if os.lang == 'fa':
                            message = f'پاسخ شما برای دانشجو {s.name} {s.last_name} ثبت شد'
                        else:
                            message = f'Your Answer For {s.name} {s.last_name} Has Been Confirmed Successfully'

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
                            if os.lang == 'fa':
                                vaziat = 'تایید شده'
                            else:
                                vaziat = 'Has Been Accepted'
                            color2 = 'green'
                        elif e.reject == True:
                            if os.lang == 'fa':
                                vaziat = 'رد شده است'
                            else:
                                vaziat = 'Has Been Rejected'
                            color2 = 'red'
                        else:
                            if os.lang == 'fa':
                                vaziat = 'در حال بررسی'
                            else:
                                vaziat = 'Has Been Pending'
                            color2 = 'black'
                        if os.lang == 'fa':
                            error_message = 'لطفااعتراض را رد یا تایید کنید'
                        else:
                            error_message = 'Please Accept or Reject The Protest'

                        context = {'ostad':os,'vahed':vahed1,'nomre':nomre1,'eteraz':e,'vaziat':vaziat,'color2':color2,'student':s,'error_message':error_message }
                        return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
                    

                    
class Eteraz5View(generic.TemplateView):
    template_name = 'uni/eteraz5.html'
    # template_name = 'uni/eteraz5_en.html'

    def get(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated: 
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id,eteraz_id):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
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
                if os.lang == 'fa':
                    message = f'نمره جدید دانشجو ثبت شد'
                else:
                    message = f"Student's New Score Confirmed"
                response = HttpResponseRedirect(reverse('uni:messageos',args = [os.id,message]))
                return response
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))


                

class MessageboxsView(generic.TemplateView):
    template_name = 'uni/messages.html'
    # template_name = 'uni/messages_en.html'

    def get(self,request,student_id,message):
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(s,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie) and request.user.is_authenticated:
            context = {'student':s,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(s)
            return HttpResponseRedirect(reverse('uni:home'))

class MessageboxaView(generic.TemplateView):
    template_name = 'uni/messagea.html'
    # template_name = 'uni/messagea_en.html'

    def get(self,request,admin_id,message):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            context = {'admin':a,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))

class MessageboxosView(generic.TemplateView):
    template_name = 'uni/messageos.html'
    # template_name = 'uni/messageos_en.html'

    def get(self,request,ostad_id,message):
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie) and request.user.is_authenticated:
            context = {'ostad':os,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(os)
            return HttpResponseRedirect(reverse('uni:home'))




class MessageboxledView(generic.TemplateView):
    template_name = 'uni/messageled.html'
    # template_name = 'uni/messageled_en.html'

    def get(self,request,leader_id,message):
        led = Leader.objects.get(pk = leader_id)
        self.template_name = changetemplate(led,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            context = {'leader':led,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))



class MessageboxbsView(generic.TemplateView):
    template_name = 'uni/messagebs.html'
    # template_name = 'uni/messagebs_en.html'

    def get(self,request,boss_id,message):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            context = {'boss':bs,'message':message}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))





    

class CreatebossView(generic.TemplateView):
    
    template_name = 'uni/createboss.html'
    # template_name = 'uni/createboss_en.html'
    
    
    def get(self,request ,leader_id):
        led = Leader.objects.get(pk = leader_id)
        self.template_name = changetemplate(led,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            if led.lang == 'fa':
                form = sabtform3()
            else:
                form = sabtform3_en()
                
            context = {'form':form,'leader':led}
            return render(request ,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        self.template_name = changetemplate(led,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if led.lang == 'fa':
            form = sabtform3(request.POST)
        else:
            form = sabtform3_en(request.POST)

        if CheckCookie(led,cookie) and request.user.is_authenticated:
            if form.is_valid():
                
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                ac = Account.objects.filter(username = z).first()
                if ac:
                    
                    if led.lang == 'fa':
                        error_message = 'این کد کاربری در حال حاضر موجود میباشد'
                    else:
                        error_message = 'This user code is in use'
                    context = {'form':form,'leader':led,'error_message':error_message}
                    return render(request ,self.template_name,context)

                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                        if led.lang == 'fa':
                            error_message = 'لطفا فرم را کامل پر کنید'
                        else:
                            error_message = 'Please Complete The Form'

                        context = {'form':form,'leader':led,'error_message':error_message}
                        return render(request ,self.template_name,context)
                
                uni2 = form.cleaned_data['uni']
                if Boss.objects.filter(uni = uni2).first():
                    if led.lang == 'fa':
                        error_message = 'ادمین دانشگاه وجود دارد'
                    else:
                        error_message = 'University Admin Exists'
                    
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
                if led.lang == 'fa':
                    message = 'ادمین با موفقیت ثبت شد'
                else:
                    message = 'Admin Added Successfully'

                return HttpResponseRedirect(reverse('uni:messageled',args = [led.id,message]))
            if form.is_valid() == False:
                if led.lang == 'fa':
                    error_message = f'لطفا فرم را کامل پر کنید'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'leader':led,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))










class CreateadminView(generic.TemplateView):
    
    template_name = 'uni/createadmin.html'
    # template_name = 'uni/createadmin_en.html'
    
    
    def get(self,request ,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if bs.lang == 'fa':
                form = sabtform4()
            else:
                form = sabtform4_en()
            context = {'form':form,'boss':bs}
            return render(request ,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if bs.lang == 'fa':
            form = sabtform4(request.POST)
        else:
            form = sabtform4_en(request.POST)
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if form.is_valid():
                
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                ac = Account.objects.filter(username = z).first()
                if ac:
                    
                    if bs.lang == 'fa':
                        error_message = 'این کد کاربری در حال حاضر موجود میباشد'
                    else:
                        error_message = 'This user code is in use'
                    context = {'form':form,'boss':bs,'error_message':error_message}
                    return render(request ,self.template_name,context)

                
                
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                        if bs.lang == 'fa':
                            error_message = 'لطفا فرم را کامل پر کنید'
                        else:
                            error_message = 'Please Complete The Form'

                        context = {'form':form,'boss':bs,'error_message':error_message}
                        return render(request ,self.template_name,context)
                
                uni2 = bs.uni
                college2 = form.cleaned_data['College']
                if Admin2.objects.filter(uni = uni2,College = college2).first():
                    if bs.lang == 'fa':
                        error_message = 'ادمین دانشکده وجود دارد'
                    else:
                        error_message = 'College Admin Exists'

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
                if bs.lang == 'fa':
                    message = 'ادمین با موفقیت ثبت شد'
                else:
                    message = 'Admin Added Successfully'
                return HttpResponseRedirect(reverse('uni:messagebs',args = [bs.id,message]))
            if form.is_valid() == False:
                if bs.lang == 'fa':
                    error_message = f'لطفا فرم را کامل پر کنید'
                else:
                    error_message = f'Please Complete The Form'
                context = {'form':form,'boss':bs,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))



    
class StudentsbsView(generic.TemplateView):
    template_name = 'uni/studentsbs.html'
    # template_name = 'uni/studentsbs_en.html'
    
   
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
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
        self.template_name = changetemplate(bs,self.template_name)
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
    # template_name = 'uni/studentbs_en.html'
    
    
    def get(self,request,boss_id,student_id):
        s = Student.objects.get(pk = student_id)
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            global gb
            if gb == 1:
                if bs.lang == 'fa':
                    messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                else:
                    messages.success(request, 'Password Has Been Changed Successfully')
                gb = 0
            context = {'boss':bs,'student':s}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




class AboutSbsView(generic.TemplateView):#student info page in ostad
    
    template_name = 'uni/aboutSbs.html'
    # template_name = 'uni/aboutSbs_en.html'

    def get(self,request,boss_id,student_id):
        
        bs = Boss.objects.get(pk = boss_id)
        s = Student.objects.get(pk = student_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if bs.lang == 'fa':
                uni2 = unidict[s.uni]
                college2 = collegedict[s.College]
                field2 = fielddict[s.field]
            else:
                uni2 = unidict_en[s.uni]
                college2 = collegedict_en[s.College]
                field2 = fielddict_en[s.field]

            context = {'student':s,'boss':bs,'uni':uni2,'college':college2,'field':field2}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))







class VahedbsView(generic.TemplateView):
    template_name = 'uni/vahedbs.html'
    # template_name = 'uni/vahedbs_en.html'

    def get(self,request,boss_id,student_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            s = Student.objects.get(pk = student_id)
            if bs.lang == 'fa':
                
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}

                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                

                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
           
            
            
            
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
                
                if bs.lang == 'fa':
                    dars2 = darsdict[y.dars]
                else:
                    dars2 = darsdict_en[y.dars]
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
                    if bs.lang == 'fa':
                        college2 = collegedict[i.college]

                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict_en[i.college]

                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3,sexdict[y.sex],dars2])
            
            context = {'student':s,'boss':bs,'vaheds':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




        







class KarnamebsView(generic.TemplateView):
    template_name = 'uni/karnamebs.html'
    # template_name = 'uni/karnamebs_en.html'

    def get(self,request,boss_id,student_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
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
                    if bs.lang == 'fa':
                        vaziat = 'قبول'
                    else:
                        vaziat = 'Accepted'
                    color2 = 'green'
                elif float(list2[1]) < 10:
                    if bs.lang == 'fa':
                        vaziat = 'مردود'
                    else:
                        vaziat = 'Rejected'
                    color2 = 'red'
                if bs.lang == 'fa':
                    dars2 = darsdict[vahed1.dars]
                else:
                    dars2 = darsdict_en[vahed1.dars]

                final_list.append([vahed1,list2[1],exam2,exam3,vaziat,color2,dars2])
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
    # template_name = 'uni/adminsbs_en.html'
    
   
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
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
        self.template_name = changetemplate(bs,self.template_name)
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
    # template_name = 'uni/adminbs_en.html'
    
    
    def get(self,request,boss_id,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            global gb
            if gb == 1:
                if bs.lang == 'fa':
                    messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                else:
                    messages.success(request, 'Password Has Been Changed Successfully')
                gb = 0
            if bs.lang == 'fa':
                college2 = collegedict[a.College]
            else:
                college2 = collegedict_en[a.College]
            context = {'boss':bs,'admin':a,'college':college2}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))


class Vahedbs2View(generic.TemplateView):
    template_name = 'uni/vahedbs2.html'
    # template_name = 'uni/vahedbs2_en.html'

    def get(self,request,boss_id,admin_id):
        bs = Boss.objects.get(pk = boss_id)
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if bs.lang == 'fa':
                
                sexdict = {'1':'موئنث' , '2':'مذکر','3':'مشترک'}

                dictime = {'01':'شنبه 8-10','02':'شنبه 10-12','03':'شنبه 13-15','04':'شنبه 15-17','05':'شنبه 17-19',
                    '11':'یکشنبه 8-10','12':'یکشنبه 10-12','13':'یکشنبه 13-15','14':'یکشنبه 15-17','15':'یکشنبه 17-19',
                    '21':'دوشنبه 8-10','22':' دوشنبه 10-12 ','23':'دوشنبه 13-15','24':'دوشنبه 15-17','25':'دوشنبه 17-19',
                    '31':'سه شنبه 8-10','32':'سه شنبه 10-12','33':'سه شنبه 13-15','34':'سه شنبه 15-17','35':'سه شنبه 17-19',
                    '41':'چهارشنبه 8-10','42':'چهارشنبه 10-12','43':'چهارشنبه 13-15','44':'چهارشنبه 15-17','45':'چهارشنبه  17-19',}
            else:
                

                sexdict = {'1':'female','2':'male','3':'Both'}
                dictime = {'01':'Saturday 8-10','02':'Saturday 10-12','03':'Saturday 13-15','04':'Saturday 15-17','05':'Saturday 17-19',
                '11':'Sunday 8-10','12':'Sunday 10-12','13':'Sunday 13-15','14':'Sunday 15-17','15':'Sunday 17-19',
                '21':'Monday 8-10','22':' Monday 10-12 ','23':'Monday 13-15','24':'Monday 15-17','25':'Monday 17-19',
                '31':'Tuesday 8-10','32':'Tuesday 10-12','33':'Tuesday 13-15','34':'Tuesday 15-17','35':'Tuesday 17-19',
                '41':'Wednesday 8-10','42':'Wednesday 10-12','43':'Wednesday 13-15','44':'Wednesday 15-17','45':'Wednesday  17-19',}
           
            
            
            vahed1 = Vahed.objects.filter(active = True,uni = bs.uni,college = a.College)
            lastlist = []
            
            for y in vahed1:
                if bs.lang == 'fa':
                    dars2 = darsdict[y.dars]
                else:
                    dars2 = darsdict_en[y.dars]

                
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
                    if bs.lang == 'fa':
                        college2 = collegedict[i.college]
                        kj = 'طبقه' +' '+ i.floor +' '+ college2 +' '+ 'کلاس' +' '+ i.number
                    else:
                        college2 = collegedict[i.college]
                        kj = 'Floor' +' '+ i.floor +' '+ college2 +' '+ 'Class' +' '+ i.number
                    list5.append(kj)
                for i in range(len(list4)):
                    dic2[list4[i]] = list5[i]
                    
                if y.exam:
                    exam2 = JalaliDateTime(y.exam).strftime("%Y/%m/%d")
                    exam3 = JalaliDateTime(y.exam).strftime("%H:%M")
                else:
                    exam2 = None
                    exam3 = None
                lastlist.append([y,dic2,list4,exam2,exam3,sexdict[y.sex],dars2])
                 
            context = {'admin':a,'lastlist':lastlist,'boss':bs}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))

class EjazeView(generic.TemplateView):
    template_name = 'uni/ejaze.html'
    # template_name = 'uni/ejaze_en.html'

    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
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
        self.template_name = changetemplate(a,self.template_name)
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
                if a.lang == 'fa':
                    message = 'دسترسی انتخاب واحد ثبت شد'
                else:
                    message = 'Unit Selection Access Registered'
                
                return HttpResponseRedirect(reverse('uni:messagea',args = [a.id,message]))
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))



class ChangePassbsView(generic.TemplateView):#change password by student
    template_name = 'uni/changepassbs.html'
    # template_name = 'uni/changepassbs_en.html'
    
    def get(self,request,boss_id):
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if bs.lang == 'fa':
                form = ChangePass()
            else:
                form = ChangePass_en()
            context = {'boss':bs,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,boss_id):
        
        bs = Boss.objects.get(pk = boss_id)
        self.template_name = changetemplate(bs,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(bs,cookie) and request.user.is_authenticated:
            if bs.lang == 'fa':
                form = ChangePass(request.POST)
            else:
                form = ChangePass_en(request.POST)
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
                        if bs.lang == 'fa':
                            error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        else:
                            error_message = 'New Passwords Must Be Same.'
                        
                        context = {'boss':bs,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    if bs.lang == 'bs':
                        error_message = f'پسوورد قدیمی نادرست است. '
                    else:
                        error_message = f'Your Old Password Is Not True'
                    context = {'boss':bs,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                if bs.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'boss':bs,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(bs)
            return HttpResponseRedirect(reverse('uni:home'))




class ChangePassledView(generic.TemplateView):#change password by student
    template_name = 'uni/changepassled.html'
    # template_name = 'uni/changepassled.html'
    
    def get(self,request,leader_id):
        led = Leader.objects.get(pk = leader_id)
        self.template_name = changetemplate(led,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            if led.lang == 'fa':
                form = ChangePass()
            else:
                form = ChangePass_en()

            context = {'leader':led,'form':form,}
            return render(request,self.template_name,context)
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,leader_id):
        
        led = Leader.objects.get(pk = leader_id)
        self.template_name = changetemplate(led,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(led,cookie) and request.user.is_authenticated:
            if led.lang == 'fa':
                form = ChangePass(request.POST)
            else:
                form = ChangePass_en(request.POST)
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
                        if led.lang == 'fa':
                            error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        else:
                            error_message = 'New Passwords Must Be Same.'
                        context = {'leader':led,'form':form,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    if led.lang == 'fa':
                        error_message = f'پسوورد قدیمی نادرست است. '
                    else:
                        error_message = f'Your Old Password Is Not True'
                    context = {'leader':led,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                if led.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'

                context = {'form':form,'leader':led,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(led)
            return HttpResponseRedirect(reverse('uni:home'))


class ForgetpassView(generic.TemplateView):
    template_name = 'uni/forget.html'
    def get(self,request,lang):
        if lang == 'fa':
            pass
        else:
            self.template_name = 'uni/forget_en.html'

        
        return render(request,self.template_name,{'lang':lang})
    def post(self,request,lang):
        
        if request.method == 'POST':
            username = request.POST.get('forget')
            try:
                aco2 = Account.objects.filter(username = username).first()
            except FieldError:
                if lang == 'fa':
                    error_message = 'همچین اکانتی وجود ندارد'
                else:
                    error_message = 'Wrong Username' 
                return render(request,self.template_name,{'error_message':error_message,'lang':lang})
            if aco2:
                if aco2.is_student:
                    s = Student.objects.filter(username = username).first()
                    f = Forget.objects.filter(username = username,check = False,s = True).first()
                    if f:
                        if lang == 'fa':
                            error_message = 'پیام شما قبلا فرستاده شده است'
                        else:
                            error_message = 'Your message has already been sent' 
                        return render(request,self.template_name,{'error_message':error_message,'lang':lang})
                    f = Forget(username = username,uni = s.uni,college = s.College,s = True,public_date = dt.datetime.now())
                    f.save()
                elif aco2.is_admin2:
                    if lang == 'fa':
                        error_message = 'همچین اکانتی وجود ندارد'
                    else:
                        error_message = 'Wrong Username' 
                    return render(request,self.template_name,{'error_message':error_message,'lang':lang})
                    
                elif aco2.is_boss:
                    if lang == 'fa':
                        error_message = 'همچین اکانتی وجود ندارد'
                    else:
                        error_message = 'Wrong Username' 
                    return render(request,self.template_name,{'error_message':error_message,'lang':lang})
                elif aco2.is_ostad:
                    os = Ostad.objects.filter(username = username).first()
                    f = Forget.objects.filter(username = username,check = False,os = True).first()
                    if f:
                        if lang == 'fa':
                            error_message = 'پیام شما قبلا فرستاده شده است'
                        else:
                            error_message = 'Your message has already been sent' 
                        return render(request,self.template_name,{'error_message':error_message,'lang':lang})
                    f = Forget(username = username,uni = os.uni,os = True,public_date = dt.datetime.now())
                    f.save()
                else:
                    if lang == 'fa':
                        error_message = 'همچین اکانتی وجود ندارد'
                    else:
                        error_message = 'Wrong Username' 
                    return render(request,self.template_name,{'error_message':error_message,'lang':lang})
                if aco2.lang == 'fa':
                    message = 'پیام شما ثبت شد'
                else:
                    message = 'your message sent'
                return HttpResponseRedirect(reverse('uni:messagef',args = [message , lang]))
                
                
            else:
                if lang == 'fa':
                    error_message = 'همچین اکانتی وجود ندارد'
                else:
                    error_message = 'Wrong Username' 
                return render(request,self.template_name,{'error_message':error_message,'lang':lang})


class MessageboxfView(generic.TemplateView):
    template_name = 'uni/messagef.html'
    # template_name = 'uni/messagesf_en.html'

    def get(self,request,message,lang):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        aco = Account.objects.filter(ip_address = ip_address).first()
        self.template_name = changetemplate(aco,self.template_name)
        context = {'message':message,'lang':lang}
        return render(request,self.template_name,context)

class Forgetpass2View(generic.TemplateView):
    template_name = 'uni/forget2.html'
    def get(self,request,admin_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:

            fs1 = Forget.objects.filter(uni = a.uni,college = a.College)
            fs2 = Forget.objects.filter(uni = a.uni,os = True)
            fs = []
            for i in fs1:
                fs.append(i)
            for i in fs2:
                fs.append(i)
            lastlist = []
            for i in fs:
                if i.s:
                    user = Student.objects.filter(uni = a.uni,College = a.College,username = i.username).first()
                elif i.os:
                    user = Ostad.objects.filter(uni = a.uni,username = i.username).first()

                if i.check:
                    if a.lang == 'fa':
                        vaziat = 'برسی شده'
                    else:
                        vaziat = 'Reviewed'
                elif not i.check:
                    if a.lang == 'fa':
                        vaziat = 'در حال بررسی'
                    else:
                        vaziat = 'Pending'
                lastlist.append([user,i,vaziat])

            context = {'admin':a,'forgets':lastlist}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))




class Forgetpass3View(generic.TemplateView):
    template_name = 'uni/forget3.html'
    
    
    def get(self,request,admin_id,ostad_id):
        a = Admin2.objects.get(pk = admin_id)
        self.template_name = changetemplate(a,self.template_name)
        os = Ostad.objects.get(pk = ostad_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = ChangePass2()
            else:
                form = ChangePass2_en()

            context = {'admin':a,'form':form}
            return render(request,self.template_name,context)
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,ostad_id):
        
        a = Admin2.objects.get(pk = admin_id)
        os = Ostad.objects.get(pk = ostad_id)
        self.template_name = changetemplate(os,self.template_name)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie) and request.user.is_authenticated:
            if a.lang == 'fa':
                form = ChangePass2(request.POST)
            else:
                form = ChangePass2_en(request.POST)

            if form.is_valid():
                
                if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                    
                    Ostad.objects.filter(pk = ostad_id).update(password = oracle10.hash(form.cleaned_data['pass2'],user=os.username))
                    os = Ostad.objects.filter(pk = ostad_id).first()
                    t = Account.objects.filter(username = os.username).first()
                    t.set_password(form.cleaned_data['pass3'])
                    t.save()
                    os.save()

                    global gb
                    gb = 1
                    if request.method == 'POST':
                        f2 = request.POST.get('forget')
                        if f2 == '1':
                            f1 = Forget.objects.filter(uni = os.uni,username = os.username,check = False,os = True).first()
                            if f1:
                                f1.check = True
                                f1.save()

                    return HttpResponseRedirect(reverse('uni:page2',args = [a.id]))
                else:
                    if a.lang == 'fa':
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                    else:
                        error_message = 'New Passwords Must Be Same.'
                    context = {'form':form,'admin':a,'error_message':error_message}
                    return render(request,self.template_name,context)
                
            else:
                if a.lang == 'fa':
                    error_message = 'لطفا فرم را کامل پر کنید.'
                else:
                    error_message = 'Please Complete The Form'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            logout2(a)
            return HttpResponseRedirect(reverse('uni:home'))
        
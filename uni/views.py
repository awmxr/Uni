from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect

from .models import Student,Admin,Exter, Ostad,Exter2,Elam,Klass
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,Loginform2,sabtform,ChangeForm,ChangePass,Change2Form,ChangePass2,sabtform2,darsform,ElamForm,KlassForm

from .models import Student,Admin,Exter, Ostad,Exter2,Elam
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,Loginform2,sabtform,ChangeForm,ChangePass,Change2Form,ChangePass2,sabtform2,darsform,ElamForm

from django.contrib import messages
from passlib.hash import oracle10
from . import choices
from django import forms
import datetime as dt
from .cookie import CheckCookie,MakeCookie
from django.contrib import messages
gb = 0 #use for message: if gb == 1: message is exist


class HomeView(generic.TemplateView):
    template_name = 'uni/home.html'
    if Exter.objects.all() :
        # if Exter.objects.all().first().number == '1':
        def get(self, request):
            global gb
            if gb == 1:
                messages.success(request, '.پسوورد با موفقیت تغییر کرد لطفا دوباره وارد شوید')
                gb = 0

            Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(online = False)
            Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(online = False)
            Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(online = False)
            response = render(request,self.template_name,{})
            response.set_cookie('access',None)
            return response
        def post(self,request):
            Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(online = False)
            Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(online = False)
            Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(online = False)
            response = render(request,self.template_name,{})
            response.set_cookie('access',None)
            return response
        
        

class PageView(generic.ListView):#student page
    context_object_name = 'student'
    template_name = 'uni/page.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s
    def get(self,request,student_id):
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie):
            return render(request,self.template_name,{'student':s})
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        if CheckCookie(s,request.COOKIES.get('access')):
            return render(request,self.template_name,{'student':s})
        else:
            return HttpResponseRedirect(reverse('uni:home'))



            
    def ren(self,request):
        return render(request ,'uni/page.html',{})

class Page2View(generic.ListView):#admin page
    context_object_name = 'admin'
    template_name = 'uni/page2.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s
    
    def get(self,request,admin_id):
        
        # messages.success(request, 'Email sent successfully.')
        s = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        Admins = Admin.objects.all()
        Students = Student.objects.all()
        cookie  = str(request.COOKIES.get('access'))
        d = CheckCookie(s,cookie)
        if d:
            return render(request,self.template_name,{'admin':s,'Admins':Admins,'Students':Students})
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        # messages.success(request, 'Email sent successfully.')
        s = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        Admins = Admin.objects.all()
        Students = Student.objects.all()
        cookie  = str(request.COOKIES.get('access'))
        d = CheckCookie(s,cookie)
        if d:
            return render(request,self.template_name,{'admin':s,'Admins':Admins,'Students':Students})
        else:
            return HttpResponseRedirect(reverse('uni:home'))


class Page3View(generic.ListView):#ostad page
    context_object_name = 'ostad'
    template_name = 'uni/page3.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id):
        q = Exter2.objects.all()[0]
        w = Elam.objects.filter(username = q.username , ostad = q.ostad,college = q.college,dars = q.dars).first()
        if w and w.time == '':
            w.delete()
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie):
            return render(request,self.template_name,{'ostad':os})
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        if CheckCookie(os,request.COOKIES.get('access')):
            return render(request,self.template_name,{'ostad':os})
        else:
            return HttpResponseRedirect(reverse('uni:home'))



class AboutSView(generic.ListView):#student info page
    context_object_name = 'student'
    template_name = 'uni/aboutS.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s
    def get(self,request,student_id):
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie):
            context = {'student':s}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class AboutS3View(generic.ListView):#student info page in ostad
    context_object_name = 'ostad'
    template_name = 'uni/aboutS3.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id,student_id):
        
        os = Ostad.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            context = {'student':s,'ostad':os}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

    
class AboutS2View(generic.ListView):#student info page in admin
    context_object_name = 'admin'
    template_name = 'uni/aboutS2.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id,student_id):
        
        a = Admin.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            context = {'student':s,'admin':a}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

    
class ChangeView(generic.ListView):#change info by student
    context_object_name = 'student'
    template_name = 'uni/change.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s
    def get(self,request,student_id):
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie):
            s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
            form = ChangeForm(instance=s)
            form.student = s
            context = {'form':form,'student':s}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie):
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
class CreateView(generic.ListView):#create student by admin
    
    template_name = 'uni/create.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    
    def get(self,request ,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = sabtform()
            context = {'form':form,'admin':a}
            return render(request ,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        global v
        # v = 0
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform(request.POST)
        if CheckCookie(a,cookie):
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
        
        

        
        
    
class LoginView(generic.ListView):#login page
    
    model = Student
    template_name = 'uni/login.html'

    def get(self , request):
        Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        form = Loginform()
        form2 = Loginform2()
        context = {'form' : form , 'form2' : form2 }
        response = render(request,self.template_name,context)
        response.set_cookie('access',None)
        return response
        
    def post(self,request):
        Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        form = Loginform(request.POST)
        form2 = Loginform2(request.POST)
        
        if (form.is_valid() and form2.is_valid()):
            users = Student.objects.all()
            for user in users:
                if user.username == form.cleaned_data['username'] :
                    if user.password == oracle10.hash(form2.cleaned_data['password'], user = user.username):
                        Student.objects.filter(username = form.cleaned_data['username']).update(login_date = dt.datetime.now())
                        Student.objects.filter(username = form.cleaned_data['username']).update(login_times = str(int(user.login_times)+ 1))
                        Student.objects.filter(username = form.cleaned_data['username']).update(online = True)
                        h = Student.objects.filter(username = form.cleaned_data['username']).first()
                        Exter.objects.all().delete()
                        q = Exter(exter_name = form.cleaned_data['username'], number = '1') 
                        q.save()
                        response = HttpResponseRedirect(reverse('uni:page',args = [user.id]))
                        response.set_cookie('access',MakeCookie(h))
                        return response
                    break
        
            users2 = Admin.objects.all()
            for user in users2:
                if user.username == form.cleaned_data['username'] :
                    if user.password == oracle10.hash(form2.cleaned_data['password'], user = user.username):
                        Admin.objects.filter(username = form.cleaned_data['username']).update(login_date = dt.datetime.now())
                        Admin.objects.filter(username = form.cleaned_data['username']).update(login_times = str(int(user.login_times)+ 1))
                        Admin.objects.filter(username = form.cleaned_data['username']).update(online = True)
                        h = Admin.objects.filter(username = form.cleaned_data['username']).first()
                        Exter.objects.all().delete()
                        q = Exter(exter_name = form.cleaned_data['username'], number = '2')
                        q.save()
                        response = HttpResponseRedirect(reverse('uni:page2',args = [user.id]))
                        response.set_cookie('access',MakeCookie(h))
                        return response
                    break

            users3 = Ostad.objects.all()
            for user in users3:
                if user.username == form.cleaned_data['username'] :
                    if user.password == oracle10.hash(form2.cleaned_data['password'], user = user.username):
                        Ostad.objects.filter(username = form.cleaned_data['username']).update(login_date = dt.datetime.now())
                        Ostad.objects.filter(username = form.cleaned_data['username']).update(login_times = str(int(user.login_times)+ 1))
                        Ostad.objects.filter(username = form.cleaned_data['username']).update(online = True)
                        h = Ostad.objects.filter(username = form.cleaned_data['username']).first()
                        Exter.objects.all().delete()
                        q = Exter(exter_name = form.cleaned_data['username'], number = '3')
                        q.save()
                        response = HttpResponseRedirect(reverse('uni:page3',args = [user.id]))
                        response.set_cookie('access',MakeCookie(h))
                        return response
                    break
                    
            error_message = "The username or password not currect"
            context = {'form' : form , 'form2' : form2 ,'error_message':error_message }
            return render(request ,'uni/login.html',context)

class ChangePassView(generic.ListView):#change password by student
    template_name = 'uni/changepass.html'
    context_object_name = 'student'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s
    def get(self,request,student_id):
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie):
            form = ChangePass()
            context = {'student':s,'form':form,}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s,cookie):
            form = ChangePass(request.POST)
            if form.is_valid():
                if oracle10.hash(form.cleaned_data['pass1'],user = s.username) == s.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(password = oracle10.hash(form.cleaned_data['pass2'],user=s.username))
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


class ChangePassView2(generic.ListView):#change password by admin
    template_name = 'uni/changepass2.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = ChangePass()
            context = {'admin':a,'form':form,}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = ChangePass(request.POST)
            if form.is_valid():
                if oracle10.hash(form.cleaned_data['pass1'],user = a.username) == a.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(password = oracle10.hash(form.cleaned_data['pass2'],user=a.username))
                        global gb
                        gb = 1
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'form':form,'admin':a,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'form':form,'admin':a,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'admin':a,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            return HttpResponseRedirect(reverse('uni:home'))


class ChangePassView4(generic.ListView):#change password by ostad
    template_name = 'uni/changepass4.html'
    context_object_name = 'ostad'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            form = ChangePass()
            context = {'ostad':os,'form':form,}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            form = ChangePass(request.POST)
            if form.is_valid():
                if oracle10.hash(form.cleaned_data['pass1'],user = os.username) == os.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(password = oracle10.hash(form.cleaned_data['pass2'],user=os.username))
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


class StudentsView(generic.ListView):#student list in admin
    template_name = 'uni/students.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        Students = Student.objects.filter(College = a.College)
        
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie):
            context = {'admin':a,'Students':Students}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,admin_id):
        Students = Student.objects.all()
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(a,cookie):
            c = request.POST.get('search')
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
            context = {'admin':a,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
            return response
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class Student1View(generic.ListView):#student profile in admin
    template_name = 'uni/student1.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id,student_id):
        s = Student.objects.get(pk = student_id)
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie):
            global gb
            if gb == 1:
                messages.success(request, '.پسوورد با موفقیت تغییر کرد ')
                gb = 0
            context = {'admin':a,'student':s}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))


class Student3View(generic.ListView):#student profile in ostad
    template_name = 'uni/student3.html'
    context_object_name = 'ostad'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id,student_id):
        s = Student.objects.get(pk = student_id)
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie):
            context = {'ostad':os,'student':s}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))


    
class Students3View(generic.ListView):#student list in ostad
    template_name = 'uni/students3.html'
    context_object_name = 'ostad'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id):
        Students = Student.objects.all()
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie):
            context = {'ostad':os,'Students':Students}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,ostad_id):
        Students = Student.objects.all()
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(os,cookie):
            c = request.POST.get('search')
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

class Change2View(generic.ListView):#change student's info by admin
    template_name = 'uni/change2.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id,student_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            s = Student.objects.get(pk = student_id)
            form = Change2Form(instance=s)
            form.student = s
            a = Admin.objects.get(pk = admin_id)
            context = {'form':form,'student':s,'admin':a}
            
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,student_id):
        a = Admin.objects.get(pk = admin_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = Change2Form(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            del form
            
            return HttpResponseRedirect(reverse('uni:student1',args = [a.id,s.id]))
            
        elif not form.is_valid():
            s = Student.objects.get(pk = student_id)
            a = Admin.objects.get(pk = admin_id)
            error_message = f'لطفا فرم را کامل پر کنید'
            context = {'form':form,'student':s,'error_message':error_message,'admin':a}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))



class ChangePassView3(generic.ListView):#change student's password by admin
    template_name = 'uni/changepass3.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id,student_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = ChangePass2()
            context = {'admin':a,'form':form,'student':s}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,student_id):
        
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = ChangePass2(request.POST)
            if form.is_valid():
                
                if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                    
                    Student.objects.filter(pk = student_id).update(password = oracle10.hash(form.cleaned_data['pass2'],user=s.username))
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
    


class StudentsView2(generic.ListView):#student list in student
    template_name = 'uni/students2.html'
    context_object_name = 'student'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,student_id):
        Students = Student.objects.all()
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie):
            context = {'student':s,'Students':Students}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,student_id):
        Students = Student.objects.all()
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(s,cookie):
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




class Student2View(generic.ListView):#studnet profile in student
    template_name = 'uni/student2.html'
    context_object_name = 'student'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s
    def get(self,request,student_id,student2_id):
        s2 = Student.objects.get(pk = student2_id)
        s = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s,cookie):
            context = {'student':s,'student2':s2}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class ElamView2(generic.ListView):
    template_name = 'uni/elam2.html'
    context_object_name = 'ostad'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie):
            context = {'ostad':os}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(os,cookie):
            if request.method == 'POST':
                timess = request.POST.getlist('timeclass')
                

                te = ''
                for i in timess:
                    te = te + i + ' '
                if te == '':
                    error_message = 'لطفا یک زمان را انتخاب کنید'
                    context = {'ostad':os,'error_message':error_message}
                    return render(request,self.template_name,context)
                q = Exter2.objects.all()[0]

                w = Elam.objects.filter(username = q.username , ostad = q.ostad,college = q.college,dars = q.dars,goruh = q.goruh).first()

                # w = Elam.objects.filter(username = q.username , ostad = q.ostad,college = q.college,dars = q.dars).first()

                w.time = te
                w.public_date = dt.datetime.now()
                w.save()
                response = HttpResponseRedirect(reverse('uni:page3',args = [os.id]))
                if w.time == '':
                    w.delete()
                return response
            


        else:
            return HttpResponseRedirect(reverse('uni:home'))




class CreateView2(generic.ListView):#create student by admin
    
    template_name = 'uni/create2.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    
    def get(self,request ,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(a,cookie):
            form = sabtform2()
            context = {'form':form,'admin':a}
            return render(request ,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform2(request.POST)
        if CheckCookie(a,cookie):
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

class DarsView(generic.ListView):
    template_name = 'uni/dars.html'
    context_object_name = 'ostad'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    
    def get(self,request,ostad_id):
        
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            form = darsform(instance = os)
            context = {'ostad':os,'form':form}
            return render(request , self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
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
                # Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(dars1 = d1)
                # Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(dars2 = d2)
                # Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(dars3 = d3)
                # Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).update(dars4 = d4)
                os.dars1 = d1
                os.dars2 = d2
                os.dars3 = d3
                os.dars4 = d4
                os.save()
                h = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
                
                
                
                
                return HttpResponseRedirect(reverse('uni:page3',args = [os.id]))

        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
class ElamView1(generic.ListView):
    template_name = 'uni/elam1.html'
    context_object_name = 'ostad'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return os
    def get(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            
            form = ElamForm(initial = {"username": os.username,'ostad':os,'phone':os.phone,'uni':os.uni})
            context = {'ostad':os,'form':form}
            return render(request,self.template_name,context)
            
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        

    def post(self,request,ostad_id):
        os = Ostad.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(os,cookie):
            
            form = ElamForm(request.POST,initial = {"username": os.username,'ostad':os})
            if form.is_valid():
                if form.cleaned_data['college'] == '------------------------------------------------------------------------------' or form.cleaned_data['dars'] == '------------------------------------------------------------------------------':
                    error_message = 'لطفا فرم را کامل پر کنید'
                    context = {'ostad':os,'form':form,'error_message':error_message}
                    return render(request,self.template_name,context)
                form.save()




                if Exter2.objects.all(): 
                    Exter2.objects.all().delete()
                q = Exter2(username = os.username , ostad = os,dars = form.cleaned_data['dars'],college = form.cleaned_data['college'])
                q.save()

                ww = list(Elam.objects.filter(dars = q.dars).all())
                Elam.objects.filter(username = q.username , ostad = q.ostad,college = q.college,dars = q.dars,goruh = '').update(goruh = len(ww))
                # z = Elam.objects.filter(username = q.username , ostad = q.ostad,college = q.college,dars = q.dars , goruh = len(ww)).first()
                Exter2.objects.filter(username = os.username).update(goruh = len(ww))


                return HttpResponseRedirect(reverse('uni:elam2',args = [os.id]))

            
            
            
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class BarnameView1(generic.ListView):
    template_name = 'uni/barname1.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie):
            e = Elam.objects.filter(uni = a.uni,college = a.College)
            context = {'admin':a,'Elam':e}
            return render(request,self.template_name,context)
            
            
        else:
            return HttpResponseRedirect(reverse('uni:home'))



class BarnameView2(generic.ListView):
    template_name = 'uni/barname2.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id,elam_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(a,cookie):
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



class CreateklassView(generic.ListView):
    template_name = 'uni/createklass.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return a
    def get(self,request,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        form = KlassForm(initial = {"college": a.College,'public_date':dt.datetime.now(),'uni':a.uni})
        if CheckCookie(a,cookie):
            
            context = {'admin':a,'form':form}
            return render(request,self.template_name,context)
               
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        form = KlassForm(request.POST ,initial = {"college": a.College,'public_date':dt.datetime.now()})
        if CheckCookie(a,cookie):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('uni:page2' ,args= [a.id]))

            
               
        else:
            return HttpResponseRedirect(reverse('uni:home'))


            return HttpResponseRedirect(reverse('uni:home'))



# class EraeView(generic.ListView):
#     template_name = 'uni/erae.html'
#     context_object_name = 'admin'
#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
#         return a
#     def get(self,request,amir_id,elam_id):
#         a = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
#         cookie  = str(request.COOKIES.get('access'))
#         list1 = []
#         dic = {}
#         if CheckCookie(a,cookie):
#             elam = Elam.objects.get(pk = elam_id)
#             klas = Klass.objects.filter(college = a.College)
#             for i in klas:
#                 q = i.por.split(' ')
#                 r = elam.time.split(' ')
#                 if not q:
#                     pass
#                 else:
#                     for p in q:
#                         for j in r:
#                             if p == j:
#                                 dic.update({i:p})





#             context ={'elam':elam,'admin':a}
#         else:
#             return HttpResponseRedirect(reverse('uni:home'))



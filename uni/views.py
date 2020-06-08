from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin,Exter
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,Loginform2,sabtform,ChangeForm,ChangePass,Change2Form
from django.contrib import messages
from passlib.hash import oracle10
from . import choices
from django import forms
import datetime as dt
from .cookie import CheckCookie,MakeCookie
from django.contrib import messages
gb = 0


class HomeView(generic.TemplateView):
    template_name = 'uni/home.html'
    context_object_name = 'last_obgect'
    if Exter.objects.all() :
        # if Exter.objects.all().first().number == '1':
        def get(self, request):
            global gb
            if gb == 1:
                messages.success(request, '.پسوورد با موفقیت تغییر کرد لطفا دوباره وارد شوید')
                gb = 0

            Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            response = render(request,self.template_name,{})
            response.set_cookie('access',None)
            return response
        def post(self,request):
            Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
            response = render(request,self.template_name,{})
            response.set_cookie('access',None)
            return response
        
        

class PageView(generic.ListView):
    context_object_name = 'student'
    template_name = 'uni/page.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,student_id):
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s1,cookie):
            return render(request,self.template_name,{'student':s1})
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        if CheckCookie(s1,request.COOKIES.get('access')):
            return render(request,self.template_name,{'student':s1})
        else:
            return HttpResponseRedirect(reverse('uni:home'))



            
    def ren(self,request):
        return render(request ,'uni/page.html',{})

class Page2View(generic.ListView):
    context_object_name = 'admin'
    template_name = 'uni/page2.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    
    def get(self,request,admin_id):
        
        # messages.success(request, 'Email sent successfully.')
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        Admins = Admin.objects.all()
        Students = Student.objects.all()
        cookie  = str(request.COOKIES.get('access'))
        d = CheckCookie(s1,cookie)
        if d:
            return render(request,self.template_name,{'admin':s1,'Admins':Admins,'Students':Students})
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        # messages.success(request, 'Email sent successfully.')
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        Admins = Admin.objects.all()
        Students = Student.objects.all()
        cookie  = str(request.COOKIES.get('access'))
        d = CheckCookie(s1,cookie)
        if d:
            return render(request,self.template_name,{'admin':s1,'Admins':Admins,'Students':Students})
        else:
            return HttpResponseRedirect(reverse('uni:home'))


class AboutSView(generic.ListView):
    context_object_name = 'student'
    template_name = 'uni/aboutS.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,student_id):
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            context = {'student':s1}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class AboutS2View(generic.ListView):
    context_object_name = 'admin'
    template_name = 'uni/aboutS2.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,admin_id,student_id):
        
        s1 = Admin.objects.get(pk = admin_id)
        s2 = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            context = {'student':s2,'admin':s1}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

    
class ChangeView(generic.ListView):
    context_object_name = 'student'
    template_name = 'uni/change.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,student_id):
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
            form = ChangeForm(instance=s1)
            form.student = s1
            context = {'form':form,'student':s1}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            form = ChangeForm(request.POST,instance=s1)
        if form.is_valid():
            form.save()
            # form.student = s1
            del form
            # form = ChangeForm(request.POST,instance=s1)
            return HttpResponseRedirect(reverse('uni:page',args = [s1.id]))
            # form = ChangeForm(request.POST,instance=s1)
        elif not form.is_valid():
            error_message = f'لطفا فرم را کامل پر کنید'
            context = {'form':form,'student':s1,'error_message':error_message}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
            



v = 0
class CreateView(generic.ListView):
    
    template_name = 'uni/create.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    
    def get(self,request ,admin_id):
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            form = sabtform()
            context = {'form':form,'admin':s1}
            return render(request ,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    
    def post(self,request,admin_id):
        global v
        # v = 0
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        form = sabtform(request.POST)
        if CheckCookie(s1,cookie):
            if form.is_valid():
                if form.cleaned_data['College'] == 'فنی مهندسی'  and v != 2:
                    v = 2
                    form.fields['field'].widget = forms.Select(choices= choices.field1_choices)
                    context = {'form':form,'admin':s1,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم پایه'  and v != 3:
                    v = 3
                    form.fields['field'].widget = forms.Select(choices= choices.field2_choices)
                    context = {'form':form,'admin':s1,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم اقتصادی و اداری' and v != 4:
                    v = 4
                    form.fields['field'].widget = forms.Select(choices= choices.fileld3_choices)
                    context = {'form':form,'admin':s1,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم سیاسی'  and v != 5:
                    v = 5
                    form.fields['field'].widget = forms.Select(choices= choices.fileld4_choices)
                    context = {'form':form,'admin':s1,}
                    return render(request ,self.template_name,context)
                elif form.cleaned_data['College'] == 'علوم دریایی'  and v != 6:
                    v = 6
                    form.fields['field'].widget = forms.Select(choices= choices.fileld5_choices)
                    context = {'form':form,'admin':s1,}
                    return render(request ,self.template_name,context)
                y = oracle10.hash(form.cleaned_data['password'],user = form.cleaned_data['username'])
                z = form.cleaned_data['username']
                v = 0
                for key in form.fields:
                    if form.cleaned_data[key] == '':
                        # v = 0
                        error_message = 'لطفا فرم را کامل پر کنید'
                        context = {'form':form,'admin':s1,'error_message':error_message}
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
                context = {'form':form,'admin':s1}
                return HttpResponseRedirect(reverse('uni:page2',args = [s1.id]))
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form':form,'admin':s1,'error_message':error_message}
                return render(request ,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
        

        
        
    
class LoginView(generic.ListView):
    
    model = Student
    template_name = 'uni/login.html'

    def get(self , request):
        Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        form = Loginform()
        form2 = Loginform2()
        context = {'form' : form , 'form2' : form2 }
        response = render(request,self.template_name,context)
        response.set_cookie('access',None)
        return response
        
    def post(self,request):
        Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(login_date = None)
        form = Loginform(request.POST)
        form2 = Loginform2(request.POST)
        
        if (form.is_valid() and form2.is_valid()):
            users = Student.objects.all()
            for user in users:
                if user.username == form.cleaned_data['username'] :
                    if user.password == oracle10.hash(form2.cleaned_data['password'], user = user.username):
                        Student.objects.filter(username = form.cleaned_data['username']).update(login_date = dt.datetime.now())
                        Student.objects.filter(username = form.cleaned_data['username']).update(login_times = str(int(user.login_times)+ 1))
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
                        h = Admin.objects.filter(username = form.cleaned_data['username']).first()
                        Exter.objects.all().delete()
                        q = Exter(exter_name = form.cleaned_data['username'], number = '2')
                        q.save()
                        response = HttpResponseRedirect(reverse('uni:page2',args = [user.id]))
                        response.set_cookie('access',MakeCookie(h))
                        return response
                    break
                    
            error_message = "The username or password not currect"
            context = {'form' : form , 'form2' : form2 ,'error_message':error_message }
            return render(request ,'uni/login.html',context)

class ChangePassView(generic.ListView):
    template_name = 'uni/changepass.html'
    context_object_name = 'student'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,student_id):
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            form = ChangePass()
            context = {'student':s1,'form':form,'student':s1}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,student_id):
        
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            form = ChangePass(request.POST)
            if form.is_valid():
                if oracle10.hash(form.cleaned_data['pass1'],user = s1.username) == s1.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        Student.objects.filter(username = Exter.objects.all()[0].exter_name).update(password = oracle10.hash(form.cleaned_data['pass2'],user=s1.username))
                        global gb
                        gb = 1
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'student':s1,'form':form,'student':s1,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'student':s1,'form':form,'student':s1,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'student':s1,'form':form,'student':s1,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            return HttpResponseRedirect(reverse('uni:home'))


class ChangePassView2(generic.ListView):
    template_name = 'uni/changepass2.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,admin_id):
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            form = ChangePass()
            context = {'admin':s1,'form':form,}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id):
        
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            form = ChangePass(request.POST)
            if form.is_valid():
                if oracle10.hash(form.cleaned_data['pass1'],user = s1.username) == s1.password:
                    if form.cleaned_data['pass2'] == form.cleaned_data['pass3']:
                        Admin.objects.filter(username = Exter.objects.all()[0].exter_name).update(password = oracle10.hash(form.cleaned_data['pass2'],user=s1.username))
                        global gb
                        gb = 1
                        return HttpResponseRedirect(reverse('uni:home'))
                    else:
                        error_message = 'تکرار پسوورد جدید همخوانی ندارد.'
                        context = {'form':form,'admin':s1,'error_message':error_message}
                        return render(request,self.template_name,context)
                else:
                    error_message = f'پسوورد قدیمی نادرست است. '
                    context = {'form':form,'admin':s1,'error_message':error_message}
                    return render(request,self.template_name,context)
            else:
                error_message = 'لطفا فرم را کامل پر کنید.'
                context = {'form':form,'admin':s1,'error_message':error_message}
                return render(request,self.template_name,context)   
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class StudentsView(generic.ListView):
    template_name = 'uni/students.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,admin_id):
        Students = Student.objects.all()
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s1,cookie):
            context = {'admin':s1,'Students':Students}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
        
    def post(self,request,admin_id):
        Students = Student.objects.all()
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        
        if CheckCookie(s1,cookie):
            c = request.POST.get('search')
            c2 = c.split(' ')
            last = ''
            for i in range(len(c2)-1):
                if i == len(c2) - 2:
                    last = last + c2[i+1]
                else:
                    last = last + c2[i+1] + ' '
            
                
            # if len(c2) == 2:
            s2 = Student.objects.filter(name = c2[0] , last_name = last).first()
            # if len(c2) == 3:
            #     s2 = Student.objects.filter(name = c2[0] , last_name = c2[1] +' '+ c2[2]).first()

            if not s2:
                s2 = Student.objects.filter(username = c2[0]).first()
            context = {'admin':s1,'Students':Students}
            response = HttpResponseRedirect(reverse('uni:student1',args = [s1.id,s2.id]))
            return response
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class Student1View(generic.ListView):
    template_name = 'uni/student1.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,admin_id,student_id):
        s2 = Student.objects.get(pk = student_id)
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))

        if CheckCookie(s1,cookie):
            context = {'admin':s1,'student':s2}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))

class Change2View(generic.ListView):
    template_name = 'uni/change2.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        return s1
    def get(self,request,admin_id,student_id):
        s1 = Admin.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s1,cookie):
            s1 = Student.objects.get(pk = student_id)
            form = Change2Form(instance=s1)
            form.student = s1
            s2 = Admin.objects.get(pk = admin_id)
            context = {'form':form,'student':s1,'admin':s2}
            
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    def post(self,request,admin_id,student_id):
        s2 = Admin.objects.get(pk = admin_id)
        s1 = Student.objects.get(pk = student_id)
        cookie  = str(request.COOKIES.get('access'))
        if CheckCookie(s2,cookie):
            form = Change2Form(request.POST,instance=s1)
        if form.is_valid():
            form.save()
            # form.student = s1
            del form
            # form = ChangeForm(request.POST,instance=s1)
            return HttpResponseRedirect(reverse('uni:student1',args = [s2.id,s1.id]))
            # form = ChangeForm(request.POST,instance=s1)
        elif not form.is_valid():
            s1 = Student.objects.get(pk = student_id)
            s2 = Admin.objects.get(pk = admin_id)
            error_message = f'لطفا فرم را کامل پر کنید'
            context = {'form':form,'student':s1,'error_message':error_message,'admin':s2}
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('uni:home'))
    


        
        
        




        


                                                    
                    
                    

            
            
            

    




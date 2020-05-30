from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin,Exter
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,Loginform2,sabtform
from django.contrib import messages


class HomeView(generic.TemplateView):
    template_name = 'uni/home.html'
    context_object_name = 'last_obgect'


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
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        return s1
            
    def ren(self,request):
        return render(request ,'uni/page2.html',{})


class AboutSView(generic.ListView):
    context_object_name = 'student'
    template_name = 'uni/aboutS.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
        # s2 = s1[0]
        
        return s1

class CreateView(generic.ListView):
    template_name = 'uni/create.html'
    context_object_name = 'admin'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        return s1
    
    def get(self,request ,admin_id):
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        form = sabtform()
        context = {'form':form,'admin':s1}
        return render(request ,self.template_name,context)

    def post(self,request,admin_id):
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        form = sabtform(request.POST)
        if form.is_valid() == False:
            error_message = f'لطفا فرم را کامل پر کنید'
            context = {'form':form,'admin':s1,'error_message':error_message}
            return render(request ,self.template_name,context)
        form.save()
        form = sabtform()
        
        success = 'دانشجو با موفقیت ثبت شد'
        
        context = {'form':form,'admin':s1}
        return HttpResponseRedirect(reverse('uni:page2',args = [s1.id]))
        
        




class LoginView(generic.ListView):
    
    model = Student
    template_name = 'uni/login.html'

    def get(self , request):
        form = Loginform()
        form2 = Loginform2()
        context = {'form' : form , 'form2' : form2 }
        return render(request ,'uni/login.html',context)
        
    def post(self,request):

        form = Loginform(request.POST)
        form2 = Loginform2(request.POST)
        
        if (form.is_valid() and form2.is_valid()):

            
            try:
                select_choice = request.POST['tip']
            except (KeyError):
                error_message = 'You didnt select a choice.'
                context = {'form' : form , 'form2' : form2 ,'error_message':error_message }
                return render(request,self.template_name,context)
            else:
                if select_choice == "radio1":
                    users = Student.objects.all()
                    for user in users:
                        if user.username == form.cleaned_data['username'] :
                            if user.password == form2.cleaned_data['password']:
                                Exter.objects.all().delete()
                                q = Exter(exter_name = form.cleaned_data['username'], number = '1') 
                                q.save()
                                return HttpResponseRedirect(reverse('uni:page',args = [user.id]))
                            break
                    # lis1 = ['Admin','Student']
                    error_message = "The username or password not currect"
                    context = {'form' : form , 'form2' : form2 ,'error_message':error_message }
                    return render(request ,'uni/login.html',context)
                else:
                    users2 = Admin.objects.all()
                    for user in users2:
                        if user.Admin_username == form.cleaned_data['username'] :
                            if user.admin_password == form2.cleaned_data['password']:
                                Exter.objects.all().delete()
                                q = Exter(exter_name = form.cleaned_data['username'], number = '2')
                                q.save()
                                return HttpResponseRedirect(reverse('uni:page2',args = [user.id]))
                            break
                    
                    error_message = "The username or password not currect"
                    context = {'form' : form , 'form2' : form2 ,'error_message':error_message }
                    return render(request ,'uni/login.html',context)

            # lis1 = ['Admin','Student']
            # error_message = "The username or password not currect"
            # context = {'error_message':error_message,'form' : form , 'form2' : form2 , 'list1':lis1}
            # return render(request ,'uni/login.html',context)
                                                    
                    
                    

            
            
            

    




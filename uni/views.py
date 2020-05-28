from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin,Exter
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,Loginform2


class HomeView(generic.TemplateView):
    # model = Student
    template_name = 'uni/home.html'
    context_object_name = 'last_obgect'


class PageView(generic.ListView):
    # model = Student
    context_object_name = 'student'
    template_name = 'uni/page.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Student.objects.filter(student_username = Exter.objects.all()[0].exter_name).first()
        # s2 = s1[0]
        
        return s1
            
    def ren(self,request):
        return render(request ,'uni/page.html',{})

class Page2View(generic.ListView):
    # model = Student
    context_object_name = 'admin'
    template_name = 'uni/page2.html'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        # s2 = s1
        # Exter.objects.all().delete()
        return s1
            
    def ren(self,request):
        return render(request ,'uni/page2.html',{})

class LoginView(generic.ListView):
    
    model = Student
    template_name = 'uni/login.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Student.objects.filter(pub_date__lte=timezone.now())

    def get(self , request):
        form = Loginform()
        form2 = Loginform2()
        list1 = ['Admin','Student']
        context = {'form' : form , 'form2' : form2 ,'lis1':list1}
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
                        if user.student_username == form.cleaned_data['username'] :
                            if user.student_password == form2.cleaned_data['password']:
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
                                                    
                    
                    

            
            
            

    




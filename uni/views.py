from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student,Admin,Exter
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform,Loginform2,sabtform


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
        s1 = Student.objects.filter(username = Exter.objects.all()[0].exter_name).first()
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
        # s2 = s1
        # Exter.objects.all().delete()
        # admin = s1
        return s1
    
    def get(self,request ,admin_id):
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        form1 = sabtform()
        form2 = sabtform()
        form3 = sabtform()
        form4 = sabtform()
        form5 = sabtform()
        form6 = sabtform()
        form7 = sabtform()
        form8 = sabtform()
        form9 = sabtform()
        form10 = sabtform()
        form11 = sabtform()
        form13 = Loginform2()
        form14 = Loginform2()
        formlist = [form1,form2,form3,form4,form5,form6,form7,form8,form9,form10,form11,form13,form14]
        context = {'form1':form1,'form2':form2,'form3':form3,
        'form4':form4,'form5':form5,'form6':form6,
        'form7':form7,'form8':form8,'form9':form9,
        'form10':form10,'form11':form11,
        'form13':form13,'form14':form14 ,'admin':s1}
        return render(request ,self.template_name,context)

    def post(self,request,admin_id):
        s1 = Admin.objects.filter(Admin_username = Exter.objects.all()[0].exter_name).first()
        form1 = sabtform(request.POST)
        form2 = sabtform(request.POST)
        form3 = sabtform(request.POST)
        form4 = sabtform(request.POST)
        form5 = sabtform(request.POST)
        form6 = sabtform(request.POST)
        form7 = sabtform(request.POST)
        form8 = sabtform(request.POST)
        form9 = sabtform(request.POST)
        form10 = sabtform(request.POST)
        form11 = sabtform(request.POST)
        form13 = Loginform2(request.POST)
        form14 = Loginform2(request.POST)
        formlist = [form1,form2,form3,form4,form5,form6,form7,form8,form9,form10,form11,form13,form14]
        for form in formlist:
            if form.is_valid() == False:
                error_message = f'لطفا فرم را کامل پر کنید'
                context = {'form1':form1,'form2':form2,'form3':form3,
                'form4':form4,'form5':form5,'form6':form6,
                'form7':form7,'form8':form8,'form9':form9,
                'form10':form10,'form11':form11,
                'form13':form13,'form14':form14 ,'admin':s1,'error_message':error_message}
                return render(request ,self.template_name,context)
        username = form1.cleaned_data['sabt']
        name =  form2.cleaned_data['sabt']
        last_name = form3.cleaned_data['sabt']
        father_name = form4.cleaned_data['sabt']
        student_live = form5.cleaned_data['sabt']
        parents_phone = form7.cleaned_data['sabt']
        phone = form6.cleaned_data['sabt']
        melli_code = form8.cleaned_data['sabt']
        field = form9.cleaned_data['sabt']
        uni = form10.cleaned_data['sabt']
        College = form11.cleaned_data['sabt']
        password = form13.cleaned_data['password']
        password2 = form14.cleaned_data['password']
        if password != password2:
            error_message = 'پسوورد نادرست است'
            form13 = Loginform2()
            form14 = Loginform2()
            return render(request ,self.template_name,context)
            
        q = Student(username = username,name = name , last_name = last_name,father_name = father_name,student_live = student_live,
        parents_phone = parents_phone,phone = phone , password = password,College = College,uni = uni,field=field,melli_code = melli_code
        ,birthday = request.POST.get('date',False) )
        q.save()
        form1 = sabtform()
        form2 = sabtform()
        form3 = sabtform()
        form4 = sabtform()
        form5 = sabtform()
        form6 = sabtform()
        form7 = sabtform()
        form8 = sabtform()
        form9 = sabtform()
        form10 = sabtform()
        form11 = sabtform()
        form13 = Loginform2()
        form14 = Loginform2()
        success = 'دانشجو با موفقیت ثبت شد'
        context = {'form1':form1,'form2':form2,'form3':form3,
                'form4':form4,'form5':form5,'form6':form6,
                'form7':form7,'form8':form8,'form9':form9,
                'form10':form10,'form11':form11,
                'form13':form13,'form14':form14 ,'admin':s1,'success':success}
        return render(request ,self.template_name,context)
        
        




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
                                                    
                    
                    

            
            
            

    




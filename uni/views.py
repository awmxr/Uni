from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import Student
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import Loginform


class HomeView(generic.ListView):
    model = Student
    template_name = 'uni/home.html'
    # context_object_name = 'latest_question_list'
    # def get_queryset(self):
    #     """
    #     Return the last five published questions (not including those set to be
    #     published in the future).
    #     """
    #     return Student.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]



class LoginView(generic.ListView):
    model = Student
    template_name = 'uni/login.html'
    def get(self , request):
        form = Loginform()
        return render(request ,self.template_name,{'form' : form})
class PageView(generic.ListView):
    model = Student
    template_name = 'uni/page.html'



# def Enter(request,user_id):
    
#     student = get_object_or_404(Student, pk=user_id)
    
    
#     return HttpResponseRedirect(reverse('uni:page', args=(student.id,)))
            
            
            

    




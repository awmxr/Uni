from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from .models import student
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class HomeView(generic.ListView):
    template_name = 'uni/home.html'
    # context_object_name = 'latest_question_list'
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return student.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]




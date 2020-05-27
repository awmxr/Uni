from django.urls import path

from . import views


app_name = 'uni'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/',views.LoginView.as_view(),name = 'login'),
    path('<int:student_id>/page/',views.PageView.as_view(),name = 'page'),
    
]
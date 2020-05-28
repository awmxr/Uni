from django.urls import path

from . import views


app_name = 'uni'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/',views.LoginView.as_view(),name = 'login'),
    path('student/<int:student_id>/page/',views.PageView.as_view(),name = 'page'),
    path('admin/<int:admin_id>/page/',views.Page2View.as_view(),name = 'page2'),
    
]
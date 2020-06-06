from django.urls import path

from . import views


app_name = 'uni'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('login/',views.LoginView.as_view(),name = 'login'), 
    path('student/<int:student_id>/page/',views.PageView.as_view(),name = 'page'),
    path('student/<int:student_id>/page/about',views.AboutSView.as_view(),name = 'aboutS'),
    path('admin/<int:admin_id>/page2/',views.Page2View.as_view(),name = 'page2'),
    path('admin/<int:admin_id>/page2/create',views.CreateView.as_view(),name = 'create'),
    path('student/<int:student_id>/page/change',views.ChangeView.as_view(),name = 'change'),
    path('student/<int:student_id>/page/changepass',views.ChangePassView.as_view(),name = 'changepass'),
    
    
]
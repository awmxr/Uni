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
    path('admin/<int:admin_id>/page2/changepass2',views.ChangePassView2.as_view(),name = 'changepass2'),
    path('admin/<int:admin_id>/page2/students',views.StudentsView.as_view(),name = 'students'),
    path('admin/<int:admin_id>/page2/students/<int:student_id>',views.Student1View.as_view(),name = 'student1'),
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2',views.AboutS2View.as_view(),name = 'aboutS2'),
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2/change2',views.Change2View.as_view(),name = 'change2'),
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2/changepass3',views.ChangePassView3.as_view(),name = 'changepass3'),
    path('student/<int:student_id>/page/students2',views.StudentsView2.as_view(),name = 'students2'),
    path('student/<int:student_id>/page/students2/<int:student2_id>',views.Student2View.as_view(),name = 'student2'),
    
    
]
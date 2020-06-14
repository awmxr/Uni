from django.urls import path

from . import views


app_name = 'uni'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), #home page
    path('login/',views.LoginView.as_view(),name = 'login'), #login page
    path('student/<int:student_id>/page/',views.PageView.as_view(),name = 'page'),#student page
    path('student/<int:student_id>/page/about',views.AboutSView.as_view(),name = 'aboutS'),#student's information page
    path('admin/<int:admin_id>/page2/',views.Page2View.as_view(),name = 'page2'),#admin's page
    path('admin/<int:admin_id>/page2/create',views.CreateView.as_view(),name = 'create'),#creat student page
    path('student/<int:student_id>/page/change',views.ChangeView.as_view(),name = 'change'),#change information page by student
    path('student/<int:student_id>/page/changepass',views.ChangePassView.as_view(),name = 'changepass'),# change password in student
    path('admin/<int:admin_id>/page2/changepass2',views.ChangePassView2.as_view(),name = 'changepass2'),# change password in admin
    path('admin/<int:admin_id>/page2/students',views.StudentsView.as_view(),name = 'students'),#students list in admin page
    path('admin/<int:admin_id>/page2/students/<int:student_id>',views.Student1View.as_view(),name = 'student1'),#student profile in admin
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2',views.AboutS2View.as_view(),name = 'aboutS2'),#student info in admin
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2/change2',views.Change2View.as_view(),name = 'change2'),#change  passwprd in admin
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2/changepass3',views.ChangePassView3.as_view(),name = 'changepass3'),#change student passwprd by admin
    path('student/<int:student_id>/page/students2',views.StudentsView2.as_view(),name = 'students2'),#student list in student
    path('student/<int:student_id>/page/students2/<int:student2_id>',views.Student2View.as_view(),name = 'student2'),#student profile in student
    path('ostad/<int:ostad_id>/page3/',views.Page3View.as_view(),name = 'page3'),#ostad page
    path('ostad/<int:ostad_id>/page3/changepass4',views.ChangePassView4.as_view(),name = 'changepass4'),# change password in ostad
    path('ostad/<int:ostad_id>/page3/students3',views.Students3View.as_view(),name = 'students3'),#students list in ostad page
    path('ostad/<int:ostad_id>/page3/students3/<int:student_id>',views.Student3View.as_view(),name = 'student3'),#student profile in ostad
    path('ostad/<int:ostad_id>/page3/students3/<int:student_id>/about3',views.AboutS3View.as_view(),name = 'aboutS3'),#student info in ostad
    path('ostad/<int:ostad_id>/page3/elam',views.ElamView.as_view(),name = 'elam'),
    path('admin/<int:admin_id>/page2/create2',views.CreateView2.as_view(),name = 'create2'),#creat ostad page

]
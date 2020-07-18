from django.urls import path

from . import views


app_name = 'uni'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), #home page
    path('logout/', views.page_logout, name='logout'),
    path('login/',views.LoginView.as_view(),name = 'login'), #login page
    path('student/<int:student_id>/page/',views.PageView.as_view(),name = 'page'),#student page
    path('student/<int:student_id>/page/darkhast4',views.Darkhast4View.as_view(),name = 'darkhast4'),
    path('student/<int:student_id>/page/karname',views.KarnameView.as_view(),name = 'karname'),
    path('student/<int:student_id>/page/karname/<int:vahed_id>/eteraz',views.EterazView.as_view(),name = 'eteraz'),
    path('student/<int:student_id>/page/karname/<int:vahed_id>/eteraz2',views.Eteraz2View.as_view(),name = 'eteraz2'),
    
    path('student/<int:student_id>/page/mydars',views.MydarsView.as_view(),name = 'mydars'),
    path('student/<int:student_id>/page/mydars/<int:vahed_id>/darkhast',views.DarkhastView.as_view(),name = 'darkhast'),
    path('student/<int:student_id>/page/entekhab',views.EntekhabView.as_view(),name = 'entekhab'),
    path('student/<int:student_id>/page/entekhab2',views.Entekhab2View.as_view(),name = 'entekhab2'),
    path('student/<int:student_id>/page/entekhab2/<int:vahed_id>/entekhab3',views.Entekhab3View.as_view(),name = 'entekhab3'),
    path('student/<int:student_id>/page/about',views.AboutSView.as_view(),name = 'aboutS'),#student's information page
    path('admin/<int:admin_id>/page2/',views.Page2View.as_view(),name = 'page2'),#admin's page
    path('admin/<int:admin_id>/page2/darkhast2',views.Darkhast2View.as_view(),name = 'darkhast2'),
    path('admin/<int:admin_id>/page2/darkhast2/<int:darkhast_id>/darkhast3',views.Darkhast3View.as_view(),name = 'darkhast3'),
    path('admin/<int:admin_id>/page2/create',views.CreateView.as_view(),name = 'create'),#creat student page
    path('student/<int:student_id>/page/change',views.ChangeView.as_view(),name = 'change'),#change information page by student
    path('student/<int:student_id>/page/changepass',views.ChangePassView.as_view(),name = 'changepass'),# change password in student
    path('admin/<int:admin_id>/page2/changepass2',views.ChangePassView2.as_view(),name = 'changepass2'),# change password in admin
    path('admin/<int:admin_id>/page2/students',views.StudentsView.as_view(),name = 'students'),#students list in admin page
    path('admin/<int:admin_id>/page2/students/<int:student_id>',views.Student1View.as_view(),name = 'student1'),#student profile in admin
    path('admin/<int:admin_id>/page2/students/<int:student_id>/karname2',views.Karname2View.as_view(),name = 'karname2'),
    path('admin/<int:admin_id>/page2/students/<int:student_id>/vahed2',views.Vahed2View.as_view(),name = 'vahed2'),
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2',views.AboutS2View.as_view(),name = 'aboutS2'),#student info in admin
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2/change2',views.Change2View.as_view(),name = 'change2'),#change  passwprd in admin
    path('admin/<int:admin_id>/page2/students/<int:student_id>/about2/changepass3',views.ChangePassView3.as_view(),name = 'changepass3'),#change student passwprd by admin
    path('student/<int:student_id>/page/students2',views.StudentsView2.as_view(),name = 'students2'),#student list in student
    path('student/<int:student_id>/page/students2/<int:student2_id>',views.Student2View.as_view(),name = 'student2'),#student profile in student
    path('ostad/<int:ostad_id>/page3/',views.Page3View.as_view(),name = 'page3'),#ostad page
    path('ostad/<int:ostad_id>/page3/eteraz3',views.Eteraz3View.as_view(),name = 'eteraz3'),
    path('ostad/<int:ostad_id>/page3/eteraz3/<int:eteraz_id>/eteraz4',views.Eteraz4View.as_view(),name = 'eteraz4'),
    path('ostad/<int:ostad_id>/page3/eteraz3/<int:eteraz_id>/eteraz4/eteraz5',views.Eteraz5View.as_view(),name = 'eteraz5'),
    path('ostad/<int:ostad_id>/page3/mydars2',views.Mydars2View.as_view(),name = 'mydars2'),#ostad page
    path('ostad/<int:ostad_id>/page3/mydars2/<int:vahed_id>/nomre',views.NomreView.as_view(),name = 'nomre'),#ostad page
    path('ostad/<int:ostad_id>/page3/changepass4',views.ChangePassView4.as_view(),name = 'changepass4'),# change password in ostad
    path('ostad/<int:ostad_id>/page3/students3',views.Students3View.as_view(),name = 'students3'),#students list in ostad page
    path('ostad/<int:ostad_id>/page3/students3/<int:student_id>',views.Student3View.as_view(),name = 'student3'),#student profile in ostad
    path('ostad/<int:ostad_id>/page3/students3/<int:student_id>/about3',views.AboutS3View.as_view(),name = 'aboutS3'),#student info in ostad
    path('ostad/<int:ostad_id>/page3/elam1',views.ElamView1.as_view(),name = 'elam1'),
    path('ostad/<int:ostad_id>/page3/elam1/<str:el>/elam2',views.ElamView2.as_view(),name = 'elam2'),
    path('admin/<int:admin_id>/page2/create2',views.CreateView2.as_view(),name = 'create2'),#creat ostad page
    path('ostad/<int:ostad_id>/page3/dars',views.DarsView.as_view() ,name = 'dars'),
    path('admin/<int:admin_id>/page2/barname1',views.BarnameView1.as_view(),name = 'barname1'),
    path('admin/<int:admin_id>/page2/barname3',views.BarnameView3.as_view(),name = 'barname3'),
    path('admin/<int:admin_id>/page2/barname1/barname2/<int:elam_id>',views.BarnameView2.as_view(),name = 'barname2'),
    path('admin/<int:admin_id>/page2/barname3/barname4/<int:elam_id>',views.BarnameView4.as_view(),name = 'barname4'),
    path('admin/<int:admin_id>/page2/barname1/barname2/<int:elam_id>/erae',views.EraeView.as_view(),name = 'erae'),
    path('admin/<int:admin_id>/page2/barname1/barname2/<int:elam_id>/erae/<int:klas_id>/erae2',views.Erae2View.as_view(),name = 'erae2'),
    path('admin/<int:admin_id>/page2/createklass',views.CreateklassView.as_view(),name = 'createklass'),
    path('admin/<int:admin_id>/page2/barname1/barname2/<int:elam_id>/erae/<int:vahed_id>/nahaee',views.NahaeeView.as_view(),name = 'nahaee'),
    path('admin/<int:admin_id>/page2/vahed',views.VahedView.as_view(),name = 'vahed'),
    path('ostad/<int:ostad_id>/page3/vaziat',views.VaziatView.as_view(),name = 'vaziat'),
    path('ostad/<int:ostad_id>/page3/vaziat/<int:elam_id>/vaziat2',views.Vaziat2View.as_view(),name = 'vaziat2'),
    path('ostad/<int:ostad_id>/page3/vaziat/<int:elam_id>/vaziat2/vaziat3',views.Vaziat3View.as_view(),name = 'vaziat3'),
    path('ostad/<int:ostad_id>/page3/vaziat/<int:elam_id>/vaziat2/vaziat3/vaziat4',views.Vaziat4View.as_view(),name = 'vaziat4'),
    # path('ostad/<int:ostad_id>/page3/vaziat/<int:elam_id>/vaziat5',views.Vaziat5View.as_view(),name = 'vaziat5'),
    



]
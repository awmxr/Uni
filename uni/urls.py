from django.urls import path

from . import views

app_name = 'uni'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/',views.LoginView.as_view(),name = 'login'),
    path('login/page',views.PageView.as_view(),name = 'page'),
    # path('enter/', views.Enter, name='enter'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
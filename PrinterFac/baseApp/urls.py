from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Path is basically the URL, the view logic file and name of URL
# History is like profile

urlpatterns = [
    path('home', views.home, name='baseApp-home'),
    path('about/', views.about, name='baseApp-about'),
    path('', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='ground/login.html'), name='loginPage'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ground/logout.html'), name='logout')
]

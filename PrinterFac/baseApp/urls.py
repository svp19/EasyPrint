from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Path is basically the URL, the view logic file and name of URL
# History is like profile

urlpatterns = [
    path('home', views.home, name='baseApp-home'),
    path('about/', views.about, name='baseApp-about'),
    path('', auth_views.LoginView.as_view(template_name='ground/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

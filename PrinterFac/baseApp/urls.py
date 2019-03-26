from django.conf.urls import url
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
    path('logout/', auth_views.LogoutView.as_view(template_name='ground/logout.html'), name='logout'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='ground/password_reset/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='ground/password_reset/password_reset_done.html'),
         name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='ground/password_reset/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path(r'password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='ground/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]

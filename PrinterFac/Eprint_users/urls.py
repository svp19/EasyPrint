from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.history, name='users-history'),
    path('upload/', views.print_upload, name='users-upload'),
    path('register/', views.register, name='users-register'),
    path('profile/', views.bill, name='users-profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

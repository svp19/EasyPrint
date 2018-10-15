from django.urls import path
from . import views

#Path is basically the URL, the view logic file and name of URL
# History is like profile

urlpatterns = [
    path('', views.home, name='baseApp-home'),
    path('about/', views.about, name='baseApp-about'),
]

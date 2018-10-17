from django.urls import path
from . import views

urlpatterns = [
    path('', views.history, name='users-history'),
    path('upload/', views.print_upload, name='users-upload'),
    path('register/', views.register, name='users-register'),
]

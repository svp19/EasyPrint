from django.urls import path
from . import views

urlpatterns = [
    path('', views.history, name='users-history')
]

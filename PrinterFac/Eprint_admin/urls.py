from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    path('', views.tasks, name='admin-tasks'),
    path('<str:order_by>', views.tasks, name='admin-tasks'),
    path('update/', views.update_prices, name='admin-update')
]


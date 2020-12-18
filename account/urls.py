from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('', views.userinfo, name='index'),
    path('certisuccess/', views.certi_success, name='certi_success')
]
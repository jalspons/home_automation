from django.contrib.auth import views as auth_views
from django.urls import include,path

from . import views

app_name = 'dashboard'
urlpatterns = [
        path('', views.index, name='index'),
        path('form/', views.activation_create_view, name='activation_form')
]


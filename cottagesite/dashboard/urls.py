from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('form1/', views.activation_create_view, name='activation'),
        path('form/', views.ActivationCreateView.as_view(), name='activation-create'),
#        path('outlet/<int:outlet_number>/', views.outlet, name='outlet'),
]


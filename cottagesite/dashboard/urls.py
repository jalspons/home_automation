from django.contrib.auth import views as auth_views
from django.urls import include,path

from . import views

app_name = 'dashboard'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('form/', views.activation_create_view, name='activation_form'),
#        path('outlet/<int:outlet_number>/', views.outlet, name='outlet'),

        path('accounts/', include('django.contrib.auth.urls')),
#        path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#        path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
#        path('accounts/password_reset/', auth_views.PasswordChangeView.as_view(), name='password_reset'),
]


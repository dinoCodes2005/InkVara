"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tkinter.font import names
from django.urls import path,include
from . import views
from django.contrib.auth import views as authentication_views
from .views import register_view,edit_profile_view,CustomLoginView,CustomLogoutView,CustomPasswordChangeView

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name="login"),
    path('logout/',CustomLogoutView.as_view(template_name= 'blogHome.html'),name="logout"),
    path('register/',views.register_view,name='register'),
    path('accounts/', include('allauth.urls')),
    path('editProfile/',views.edit_profile_view,name='editProfile'),
    path('settings/<int:id>/',views.settings,name='settings'),
    path('password_change/',CustomPasswordChangeView.as_view(template_name = "password_change.html"),name='password_change'),
    path('password_change/done/', authentication_views.PasswordChangeDoneView.as_view(template_name="registration/login.html"), name='password_change_done'),
    path('password_reset/', authentication_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', authentication_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', authentication_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', authentication_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
]

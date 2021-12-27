"""fitness_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from userprofile import views, models

urlpatterns = [
    path('admin/', admin.site.urls), #afuerst / 0000
    path('', views.startpage, name="home"),
    path('contactme/', views.contact, name="contact"),

    path("logout/", views.logoutuser, name="logoutuser"),
    path("login/", views.loginuser, name="loginuser"),

    path('profile/', views.profile, name="profile"),
    path('configure-next-cycle/', views.configure, name="configure"),
    path('workout/<str:cycle>', views.workout, name="workout"),
    path('success', views.success, name="success")
]

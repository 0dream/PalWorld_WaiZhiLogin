"""
URL configuration for Pal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import log_reg

urlpatterns = [
    path('', log_reg.index_html, name='index'),
    path('login.html/', log_reg.login_html, name='login'),
    path('register.html/', log_reg.register_html, name='register'),
    path('check_login.html/', log_reg.check_login_html, name='check_login'),
    path('register_false.html/', log_reg.register_html, name='register_false'),
    #方法
    path('login/', log_reg.login, name='login'),
    path('register/', log_reg.register, name='register'),
    path('check_login/', log_reg.check_login, name='check_login'),
]

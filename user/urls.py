"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url,include
from .import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # 登录
    url(r'login/', views.login, name='login'),
    # 注册
    url(r'register/', views.register, name='register'),
    # 个人信息增删改查
    url(r'personInfo/', views.personInfo, name='personInfo'),
    # 我的个人动态
    url(r'myDynamics/(\d+)/(\d+)/', views.myDynamics, name='myDynamics'),
    # 我的关注动态
    url(r'trendsConcern/(\d+)/(\d+)/', views.trendsConcern, name='trendsConcern'),
    # 单个动态
    url(r'oneDynamic/(dynamic|dairy|test)/(\d+)/', views.oneDynamic, name='oneDynamic'),
    # 评论增删改查
    url(r'viewComment/', views.viewComment, name='viewComment'),
    # 点赞增删改查
    url(r'viewCompliment/', views.viewCompliment, name='viewCompliment'),
    # 收藏增删改查
    url(r'viewCollections/', views.viewCollections, name='viewCollections'),
    # 关注增删改查
    url(r'viewConcern/', views.viewConcern, name='viewConcern'),



]

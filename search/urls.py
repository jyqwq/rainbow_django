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
    # 普通搜索
    url(r'searchAll', views.searchAll, name='searchAll'),
    # 产品分类搜索
    url(r'searchProduct', views.searchProduct, name='searchProduct'),
    # 品牌分类搜索
    url(r'searchBrand', views.searchBrand, name='searchBrand'),
    # 成分分类搜索
    url(r'searchComponent', views.searchComponent, name='searchComponent'),
    # 效果分类搜索
    url(r'searchEffect', views.searchEffect, name='searchEffect'),
    # 品种分类搜索
    url(r'searchVarieties', views.searchVarieties, name='searchVarieties'),
    # 标签分类搜索
    url(r'searchTags', views.searchTags, name='searchTags'),
    # 搜索心情
    url(r'searchDynamic', views.searchDynamic, name='searchDynamic'),
    # 搜索日记
    url(r'searchJournal', views.searchJournal, name='searchJournal'),
    # 搜索测评
    url(r'searchTest', views.searchTest, name='searchTest'),
    # 实时热搜排行
    url(r'hotSearch', views.hotSearch, name='hotSearch'),
    # 热门日记排行
    url(r'hotDairy', views.hotDairy, name='hotDairy'),
    # 热门测评排行
    url(r'hotTest', views.hotTest, name='hotTest'),
    # 热门妆品排行
    url(r'hotCosmetics', views.hotCosmetics, name='hotCosmetics'),
    # 热搜关键字 增查
    url(r'hotKey/', views.hotKey, name='hotKey'),
    # 单个产品
    url(r'oneProduct', views.oneProduct, name='oneProduct'),
]

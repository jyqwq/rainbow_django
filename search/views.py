from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
import json
from search import models

# Create your views here.

# 搜索主页
def index(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('搜索主页错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 普通搜索
def searchAll(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('普通搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 产品分类搜索
def searchProduct(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('产品分类搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 品牌分类搜索
def searchBrand(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('品牌分类搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 品种分类搜索
def searchVarieties(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('品种分类搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 标签分类搜索
def searchTags(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('标签分类搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 搜索心情
def searchDynamic(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('搜索心情错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 搜索日记
def searchJournal(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('搜索日记错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 搜索测评
def searchTest(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('搜索测评错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 实时热搜排行
def hotSearch(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('实时热搜排行错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 热门日记排行
def hotDairy(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('热门日记排行错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 热门测评排行
def hotTest(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('热门测评排行错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 热门妆品排行
def hotCosmetics(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('热门妆品排行错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 热搜关键字 增查
def hotKey(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        try:
            pass
        except Exception as ex:
            print('热搜关键字 增查错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 单个产品
def oneProduct(request):
    if request.method == "GET":
        try:
            pass
        except Exception as ex:
            print('单个产品错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

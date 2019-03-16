from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
import json
from search import models

# Create your views here.

# 搜索主页
def index(request):
    if request.method == "GET":
        pass

# 普通搜索
def searchAll(request):
    if request.method == "GET":
        pass

# 产品分类搜索
def searchProduct(request):
    if request.method == "GET":
        pass

# 品牌分类搜索
def searchBrand(request):
    if request.method == "GET":
        pass

# 品种分类搜索
def searchVarieties(request):
    if request.method == "GET":
        pass

# 标签分类搜索
def searchTags(request):
    if request.method == "GET":
        pass

# 搜索心情
def searchDynamic(request):
    if request.method == "GET":
        pass

# 搜索日记
def searchJournal(request):
    if request.method == "GET":
        pass

# 搜索测评
def searchTest(request):
    if request.method == "GET":
        pass

# 实时热搜排行
def hotSearch(request):
    if request.method == "GET":
        pass

# 热门日记排行
def hotDairy(request):
    if request.method == "GET":
        pass

# 热门测评排行
def hotTest(request):
    if request.method == "GET":
        pass

# 热门妆品排行
def hotCosmetics(request):
    if request.method == "GET":
        pass

# 热搜关键字 增查
def hotKey(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass

# 单个产品
def oneProduct(request):
    if request.method == "GET":
        pass

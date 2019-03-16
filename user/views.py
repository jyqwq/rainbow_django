from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
import json
from user import models

# Create your views here.

# 用户主页
def index():
    pass

# 个人操作管理
# post请求
# 登录
def login(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass

# 注册
def register(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass

# 个人信息增删改查
def personInfo(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass

# 我的个人动态
def myDynamics(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass

# 我的关注动态
def trendsConcern(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass

# get请求
# 单个动态
def oneDynamic(request):
    if request.method == "GET":
        pass

# 评论增删改查
def viewComment(request):
    if request.method == "GET":
        pass

# 点赞增删改查
def viewCompliment(request):
    if request.method == "GET":
        pass

# 收藏增删改查
def viewCollections(request):
    if request.method == "GET":
        pass

# 关注增删改查
def viewConcern(request):
    if request.method == "GET":
        pass


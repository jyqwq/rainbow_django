from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
import json
from sharing import models

# Create your views here.

# 分享主页
def index(request):
    pass

# 分享发布
def releaseSharing(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        pass
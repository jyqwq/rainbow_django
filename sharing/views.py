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
        try:
            pass
        except Exception as ex:
            print('分享发布错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})
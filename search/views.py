from django.http import HttpResponse, JsonResponse
import json
from search import models
from user import models as umodels
from sharing import models as smodels
from django.db.models import Q
from django.forms.models import model_to_dict
import itertools
import operator


# Create your views here.

# 搜索主页
def index(request):
    return JsonResponse('这是搜索主页...')


# 普通搜索
def searchAll(request):
    if request.method == "GET":
        try:
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 16
                b = page * 16
                res = list(models.Commodity.objects.filter(Q(name__icontains=key) | Q(brand__icontains=key) | Q(component__icontains=key) | Q(Effect__icontains=key)).values()[a:b])
                for c in res:
                    com = models.Commodity.objects.get(id=c['id'])
                    adaptability = list(com.adaptability.all().values())
                    a = []
                    for ada in adaptability:
                        a.append(ada['skin'])
                    category = model_to_dict(models.Category.objects.get(id=c['category_id']))
                    c['category'] = category['Category']
                    c['adaptability'] = a
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 16
                b = page * 16
                res = list(models.Commodity.objects.filter(name__icontains=key).values()[a:b])
                for c in res:
                    com = models.Commodity.objects.get(id=c['id'])
                    adaptability = list(com.adaptability.all().values())
                    a = []
                    for ada in adaptability:
                        a.append(ada['skin'])
                    category = model_to_dict(models.Category.objects.get(id=c['category_id']))
                    c['category'] = category['Category']
                    c['adaptability'] = a
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 16
                b = page * 16
                res = list(models.Commodity.objects.filter(brand__icontains=key).values()[a:b])
                for c in res:
                    com = models.Commodity.objects.get(id=c['id'])
                    adaptability = list(com.adaptability.all().values())
                    a = []
                    for ada in adaptability:
                        a.append(ada['skin'])
                    category = model_to_dict(models.Category.objects.get(id=c['category_id']))
                    c['category'] = category['Category']
                    c['adaptability'] = a
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('品牌分类搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 成分分类搜索
def searchComponent(request):
    if request.method == "GET":
        try:
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 16
                b = page * 16
                res = list(models.Commodity.objects.filter(component__icontains=key).values()[a:b])
                for c in res:
                    com = models.Commodity.objects.get(id=c['id'])
                    adaptability = list(com.adaptability.all().values())
                    a = []
                    for ada in adaptability:
                        a.append(ada['skin'])
                    category = model_to_dict(models.Category.objects.get(id=c['category_id']))
                    c['category'] = category['Category']
                    c['adaptability'] = a
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('品牌分类搜索错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 效果分类搜索
def searchEffect(request):
    if request.method == "GET":
        try:
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 16
                b = page * 16
                res = list(models.Commodity.objects.filter(Effect__icontains=key).values()[a:b])
                for c in res:
                    com = models.Commodity.objects.get(id=c['id'])
                    adaptability = list(com.adaptability.all().values())
                    a = []
                    for ada in adaptability:
                        a.append(ada['skin'])
                    category = model_to_dict(models.Category.objects.get(id=c['category_id']))
                    c['category'] = category['Category']
                    c['adaptability'] = a
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 16
                b = page * 16
                id = list(models.Category.objects.filter(Category__contains=key).values())[0]
                res = list(models.Commodity.objects.filter(category_id=id['id']).values()[a:b])
                for c in res:
                    com = models.Commodity.objects.get(id=c['id'])
                    adaptability = list(com.adaptability.all().values())
                    a = []
                    for ada in adaptability:
                        a.append(ada['skin'])
                    category = model_to_dict(models.Category.objects.get(id=c['category_id']))
                    c['category'] = category['Category']
                    c['adaptability'] = a
                return JsonResponse(res,safe=False)
            else:
                return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page >0:
                a = (page - 1) * 10
                b = page * 10
                dairy = list(smodels.Dairy.objects.filter(tags__contains=key).values()[a:b])
                dynamic = list(smodels.Dynamic.objects.filter(tags__contains=key).values()[a:b])
                test = list(smodels.Test.objects.filter(tags__contains=key).values()[a:b])
                if test:
                    for t in test:
                        ts = list(smodels.TestSubtitle.objects.filter(main_id=t['id']).values())
                        t['subtitle'] = ts
                        # 合并上面三个列表并按时间排序取前十个
                res = list(reversed(sorted(list(itertools.chain(dairy, dynamic, test)), key=operator.itemgetter('date'))))[:10]
                return JsonResponse(res,safe=False)
            else:
                return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 10
                b = page * 10
                res = list(smodels.Dynamic.objects.filter(Q(tags__contains=key) | Q(content__contains=key)).values()[a:b])
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 10
                b = page * 10
                res = list(smodels.Dairy.objects.filter(Q(tags__contains=key) | Q(content__contains=key) | Q(title__contains=key)).values()[a:b])
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            key = request.GET.get('key')
            page = int(request.GET.get('page'))
            if key and page > 0:
                a = (page - 1) * 10
                b = page * 10
                test = list(smodels.Test.objects.filter(Q(tags__contains=key) | Q(content__contains=key) | Q(title__contains=key)).values()[a:b])
                if test:
                    for t in test:
                        ts = list(smodels.TestSubtitle.objects.filter(main_id=t['id']).values())
                        t['subtitle'] = ts
                        # 合并上面三个列表并按时间排序取前十个
                res = list(reversed(sorted(test, key=operator.itemgetter('date'))))[:10]
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            page = int(request.GET.get('page'))
            if page > 0:
                a = (page - 1) * 10
                b = page * 10
                dairy = list(smodels.Dairy.objects.filter().order_by('click').values()[a:b])
                dynamic = list(smodels.Dynamic.objects.filter().order_by('click').values()[a:b])
                test = list(smodels.Test.objects.filter().order_by('click').values()[a:b])
                res = list(reversed(sorted(list(itertools.chain(dairy, dynamic, test)), key=operator.itemgetter('date'))))[:10]
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            page = int(request.GET.get('page'))
            if page > 0:
                a = (page - 1) * 10
                b = page * 10
                res = list(smodels.Dairy.objects.filter().order_by('click').values()[a:b])
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            page = int(request.GET.get('page'))
            if page > 0:
                a = (page - 1) * 10
                b = page * 10
                res = list(smodels.Test.objects.filter().order_by('click').values()[a:b])
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            page = int(request.GET.get('page'))
            if page > 0:
                a = (page - 1) * 16
                b = page * 16
                res = list(models.Commodity.objects.filter().order_by('click').values()[a:b])
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
            if obtain.get('method'):
                if obtain['method'] == 'add':
                    if obtain.get('content') and obtain.get('date') or obtain.get('user_id'):
                        del obtain['method']
                        models.SearchKey.objects.create(**obtain)
                        return JsonResponse({"status_code":"10013","status_text":"记录成功"})
                    else:
                        return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
                elif obtain['method'] == 'check':
                    res = list(models.SearchKey.objects.filter().values('content').distinct())
                    for i in res:
                        r = models.SearchKey.objects.filter(content=i['content']).values().count()
                        i['count'] = r
                    resp = list(reversed(sorted(res, key=operator.itemgetter('count'))))[:20]
                    return JsonResponse(resp,safe=False)
            else:
                return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
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
            id = request.GET.get('id')
            print(id)
            res = models.Commodity.objects.filter(id=id).values().first()
            com = models.Commodity.objects.get(id=res['id'])
            adaptability = list(com.adaptability.all().values())
            a = []
            for ada in adaptability:
                a.append(ada['skin'])
            category = model_to_dict(models.Category.objects.get(id=res['category_id']))
            res['category'] = category['Category']
            res['adaptability'] = a
            return JsonResponse(res, safe=False)
        except Exception as ex:
            print('单个产品错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

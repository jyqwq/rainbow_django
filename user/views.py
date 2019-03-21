from django.http import HttpResponse, JsonResponse
import json
from user import models
from sharing import models as smodels
from search import models as semodels
from utils.token import *
from utils.user_func import *
from django.forms.models import model_to_dict
import itertools
import operator

# Create your views here.

# 用户主页
def index():
    pass


# 登录
def login(request):
    if request.method == "POST":
        user = json.loads(request.body)
        if user.get('telephone') and user.get('password'):
            res = online(user)
            if res['status_code'] == '10003':
                token = createToken(user['telephone'],res['id'])
                resp = JsonResponse(data=json.dumps({"status_code": "10003", "status_text": "登录成功","userInfo":res['userInfo']}), safe=False)
                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                return JsonResponse(res)
        else:
            return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
    else:
        return JsonResponse({"status_code":"40000","status_text":"请求方法不合法"})


# 注册
def register(request):
    if request.method == "POST":
        user = json.loads(request.body)
        if user.get('telephone') and user.get('password') and user.get('name') and user.get('register_time'):
            res = newPerson(user)
            if res.id:
                resp = JsonResponse(data=json.dumps({"status_code":"10001","status_text":"注册成功"}),safe=False)
                token = createToken(user['telephone'], res.id)
                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                return JsonResponse(res)
        else:
            return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 修改手机号
def newTel(request):
    if request.method == "POST":
        try:
            pass
        except Exception as ex:
            print('修改手机号错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 修改密码
def newPassword(request):
    if request.method == "POST":
        try:
            pass
        except Exception as ex:
            print('修改密码错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})



# 个人信息改查
def personInfo(request):
    if request.method == "POST":
        user = json.loads(request.body)
        if user.get('method') and user.get('user_id'):
            try:
                if user['method'] == 'check':
                    uu = model_to_dict(models.UserInfo.objects.get(user_id=user['user_id']))
                    return JsonResponse(uu)
                elif user['method'] == 'update':
                    id = user['user_id']
                    del user['method']
                    del user['user_id']
                    uu = models.UserInfo.objects.filter(user_id=id).update(**user)
                    if uu == 1:
                        return JsonResponse({"status_code":"10014","status_text":"更新成功"})
                    else:
                        return JsonResponse({"status_code":"40004","status_text":"系统错误"})
                else:
                    return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
            except Exception as ex:
                print('个人信息改查错误')
                print(ex)
                return JsonResponse({"status_code":"40004","status_text":"系统错误"})
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 我的个人动态
def myDynamics(request, user_id, page):
    if request.method == "GET":
        try:
            if user_id and page and int(page) >= 0:
                a = (int(page) - 1) * 10
                b = int(page) * 10
                dairy = list(smodels.Dairy.objects.filter(user_id=user_id).values()[a:b])
                dynamic = list(smodels.Dynamic.objects.filter(user_id=user_id).values()[a:b])
                test = list(smodels.Test.objects.filter(user_id=user_id).values()[a:b])
                for t in test:
                    ts = list(smodels.TestSubtitle.objects.filter(main_id=t['id']).values())
                    t['subtitle'] = ts
                # 合并上面三个列表并按时间排序取前十个
                resp = list(
                    reversed(sorted(list(itertools.chain(dairy, dynamic, test)), key=operator.itemgetter('date'))))[:10]
                return JsonResponse(resp, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('我的个人动态错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 我的关注动态
def trendsConcern(request, user_id, page):
    if request.method == "GET":
        try:
            if user_id and page and int(page) >= 0:
                a = (int(page) - 1) * 10
                b = int(page) * 10
                res = []
                # 先拉取关注列表
                concern = list(models.Followers.objects.filter(follower=user_id).values('concern_id'))
                for p in concern:
                    dairy = list(smodels.Dairy.objects.filter(user_id=p['concern_id']).values()[a:b])
                    dynamic = list(smodels.Dynamic.objects.filter(user_id=p['concern_id']).values()[a:b])
                    test = list(smodels.Test.objects.filter(user_id=p['concern_id']).values()[a:b])
                    for t in test:
                        ts = list(smodels.TestSubtitle.objects.filter(main_id=t['id']).values())
                        t['subtitle'] = ts
                    res += dairy
                    res += dynamic
                    res += test
                resp = list(reversed(sorted(res, key=operator.itemgetter('date'))))[:20]
                return JsonResponse(resp, safe=False)
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('我的关注动态错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 单个动态
def oneDynamic(request, type, id):
    if request.method == "GET":
        try:
            if type == 'dynamic':
                res = smodels.Dynamic.objects.filter(id=id).values().first()
            elif type == 'dairy':
                res = smodels.Dairy.objects.filter(id=id).values().first()
            elif type == 'test':
                res = smodels.Test.objects.filter(id=id).values().first()
                ts = list(smodels.TestSubtitle.objects.filter(main_id=res['id']).values())
                res['subtitle'] = ts
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            return JsonResponse(res)
        except Exception as ex:
            print('单个动态错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 评论增删查
def viewComment(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        try:
            if obtain.get('method'):
                # 添加评论
                if obtain['method'] == 'add':
                    if obtain.get('content') and obtain.get('type') and obtain.get('id') and obtain.get('user_id') and obtain.get('date'):
                        if obtain['type'] == 'dynamic':
                            obtain['Dynamic_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DynamicCom.objects.create(**obtain)
                        elif obtain['type'] == 'dairy':
                            obtain['Dairy_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DairyCom.objects.create(**obtain)
                        elif obtain['type'] == 'test':
                            obtain['Test_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.TestCom.objects.create(**obtain)
                        elif obtain['type'] == 'commodity':
                            obtain['commodity_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = semodels.CommodityCom.objects.create(**obtain)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res.id:
                            return JsonResponse({"status_code": "10021", "status_text": "评论成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 删除评论
                elif obtain['method'] == 'del':
                    if obtain.get('type') and obtain.get('id'):
                        if obtain['type'] == 'dynamic':
                            res = smodels.DynamicCom.objects.filter(id=obtain['id']).delete()
                        elif obtain['type'] == 'dairy':
                            res = smodels.DairyCom.objects.filter(id=obtain['id']).delete()
                        elif obtain['type'] == 'test':
                            res = smodels.TestCom.objects.filter(id=obtain['id']).delete()
                        elif obtain['type'] == 'commodity':
                            res = semodels.CommodityCom.objects.filter(id=obtain['id']).delete()
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res[0] == 1:
                            return JsonResponse({"status_code":"10010","status_text":"删除成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 查看评论
                elif obtain['method'] == 'check':
                    if obtain.get('target'):
                        if isinstance(obtain['target'], list):
                            resp = []
                            for i in obtain['target']:
                                if i.get('type') and i.get('id'):
                                    if i['type'] == 'dynamic':
                                        com = list(smodels.DynamicCom.objects.filter(Dynamic_id=i['id']).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name','icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'dairy':
                                        com = list(smodels.DairyCom.objects.filter(Dairy_id=i['id']).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'test':
                                        com = smodels.TestCom.objects.filter(Test_id=i['id']).values()
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'commodity':
                                        com = list(semodels.CommodityCom.objects.filter(commodity_id=i['id']).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name','icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    else:
                                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            return JsonResponse(resp,safe=False)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('评论增删改查错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 点赞增删改查
def viewCompliment(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        try:
            if obtain.get('method'):
                # 添加点赞
                if obtain['method'] == 'add':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id') and obtain.get('date'):
                        if obtain['type'] == 'dynamic':
                            obtain['Dynamic_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DynamicFbs.objects.create(**obtain)
                        elif obtain['type'] == 'dairy':
                            obtain['Dairy_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DairyFbs.objects.create(**obtain)
                        elif obtain['type'] == 'test':
                            obtain['Test_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.TestFbs.objects.create(**obtain)
                        elif obtain['type'] == 'commodity':
                            obtain['commodity_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = semodels.CommodityFbs.objects.create(**obtain)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res.id:
                            return JsonResponse({"status_code":"10018","status_text":"赞成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 删除点赞
                elif obtain['method'] == 'del':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id'):
                        if obtain['type'] == 'dynamic':
                            res = smodels.DynamicFbs.objects.filter(Dynamic_id=obtain['id'], user_id=obtain['user_id']).delete()
                        elif obtain['type'] == 'dairy':
                            res = smodels.DairyFbs.objects.filter(Dairy_id=obtain['id'], user_id=obtain['user_id']).delete()
                        elif obtain['type'] == 'test':
                            res = smodels.TestFbs.objects.filter(Test_id=obtain['id'], user_id=obtain['user_id']).delete()
                        elif obtain['type'] == 'commodity':
                            res = semodels.CommodityFbs.objects.filter(commodity_id=obtain['id'], user_id=obtain['user_id']).delete()
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res[0] == 1:
                            return JsonResponse({"status_code":"10010","status_text":"删除成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 查看点赞
                elif obtain['method'] == 'check':
                    if obtain.get('target'):
                        if isinstance(obtain['target'], list):
                            resp = []
                            for i in obtain['target']:
                                if i.get('type') and (i.get('id') or i.get('user_id')):
                                    if i['type'] == 'dynamic':
                                        if i.get('id'):
                                            i['Dynamic_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(smodels.DynamicFbs.objects.filter(**i).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'dairy':
                                        if i.get('id'):
                                            i['Dairy_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(smodels.DairyFbs.objects.filter(**i).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'test':
                                        if i.get('id'):
                                            i['Test_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = smodels.TestFbs.objects.filter(**i).values()
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'commodity':
                                        if i.get('id'):
                                            i['commodity_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(semodels.CommodityFbs.objects.filter(**i).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name','icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    else:
                                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            if not resp:
                                return JsonResponse({"status_code":"10020","status_text":"未赞"})
                            return JsonResponse(resp,safe=False)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('点赞增删改查错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 收藏增删改查
def viewCollections(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        try:
            if obtain.get('method'):
                # 添加收藏
                if obtain['method'] == 'add':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id') and obtain.get('date'):
                        if obtain['type'] == 'dynamic':
                            obtain['Dynamic_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DynamicCol.objects.create(**obtain)
                        elif obtain['type'] == 'dairy':
                            obtain['Dairy_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DairyCol.objects.create(**obtain)
                        elif obtain['type'] == 'test':
                            obtain['Test_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.TestCol.objects.create(**obtain)
                        elif obtain['type'] == 'commodity':
                            obtain['commodity_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = semodels.CommodityCol.objects.create(**obtain)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res.id:
                            return JsonResponse({"status_code":"10015","status_text":"收藏成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 删除收藏
                elif obtain['method'] == 'del':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id'):
                        if obtain['type'] == 'dynamic':
                            res = smodels.DynamicCol.objects.filter(Dynamic_id=obtain['id'], user_id=obtain['user_id']).delete()
                        elif obtain['type'] == 'dairy':
                            res = smodels.DairyCol.objects.filter(Dairy_id=obtain['id'], user_id=obtain['user_id']).delete()
                        elif obtain['type'] == 'test':
                            res = smodels.TestCol.objects.filter(Test_id=obtain['id'], user_id=obtain['user_id']).delete()
                        elif obtain['type'] == 'commodity':
                            res = semodels.CommodityCol.objects.filter(commodity_id=obtain['id'], user_id=obtain['user_id']).delete()
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res[0] == 1:
                            return JsonResponse({"status_code":"10010","status_text":"删除成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 查看收藏
                elif obtain['method'] == 'check':
                    if obtain.get('target'):
                        if isinstance(obtain['target'], list):
                            resp = []
                            for i in obtain['target']:
                                if i.get('type') and (i.get('id') or i.get('user_id')):
                                    if i['type'] == 'dynamic':
                                        if i.get('id'):
                                            i['Dynamic_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(smodels.DynamicCol.objects.filter(**i).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'dairy':
                                        if i.get('id'):
                                            i['Dairy_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(smodels.DairyCol.objects.filter(**i).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'test':
                                        if i.get('id'):
                                            i['Test_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = smodels.TestCol.objects.filter(**i).values()
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name', 'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'commodity':
                                        if i.get('id'):
                                            i['commodity_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(semodels.CommodityCol.objects.filter(**i).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name','icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    else:
                                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            if not resp:
                                return JsonResponse({"status_code":"10020","status_text":"未赞"})
                            return JsonResponse(resp,safe=False)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('收藏增删改查错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})

# 关注增删改查
def viewConcern(request):
    if request.method == "POST":
        obtain = json.loads(request.body)
        try:
            if obtain.get('method'):
                # 添加关注
                if obtain['method'] == 'add':
                    if obtain.get('concern_id') and obtain.get('follower_id') and obtain.get('date'):
                        del obtain['method']
                        res = models.Followers.objects.create(**obtain)
                        if res.id:
                            return JsonResponse({"status_code":"10009","status_text":"关注成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                # 删除关注
                elif obtain['method'] == 'del':
                    if obtain.get('concern_id') and obtain.get('follower_id'):
                        del obtain['method']
                        res = models.Followers.objects.filter(**obtain).delete()
                        if res.id:
                            return JsonResponse({"status_code":"10010","status_text":"删除成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                # 查看关注
                elif obtain['method'] == 'check':
                    if obtain.get('concern_id') or obtain.get('follower_id'):
                        resp = []
                        del obtain['method']
                        res = list(models.Followers.objects.filter(**obtain).values())
                        for c in res:
                            concern = models.UserInfo.objects.filter(user_id=c['concern_id']).values('name', 'icon_id').first()
                            concern_i = models.Icon.objects.filter(id=concern['icon_id']).values('icon_url').first()
                            follower = models.UserInfo.objects.filter(user_id=c['follower_id']).values('name', 'icon_id').first()
                            follower_i = models.Icon.objects.filter(id=concern['icon_id']).values('icon_url').first()
                            c['concernInfo'] = {'name': concern['name'], 'icon': concern_i['icon_url']}
                            c['followerInfo'] = {'name': follower['name'], 'icon': follower_i['icon_url']}
                            resp.append(c)
                        return JsonResponse(resp,safe=False)
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('关注增删改查错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


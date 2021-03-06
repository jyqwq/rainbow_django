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
import uuid
from django.db.models import F


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
                token = createToken(user['telephone'], res['id'])
                resp = JsonResponse(data=json.dumps({"status_code": "10003", "status_text": "登录成功", "userInfo": res['userInfo']}),safe=False)
                resp['token'] = token
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                resp = JsonResponse(data=json.dumps({"status_code": res['status_code'], "status_text": res['status_text']}),safe=False)
                resp['token'] = None
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
        elif user.get('token'):
            data = checkToken(user['token'])
            if data:
                uu = model_to_dict(models.UserInfo.objects.get(user_id=data['user_id']))
                resp = JsonResponse(
                    data=json.dumps({"status_code": "10003", "status_text": "登录成功", "userInfo": uu}),
                    safe=False)
                resp['token'] = None
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
            else:
                resp = JsonResponse(
                    data=json.dumps({"status_code": "10006", "status_text": "登录过期"}),
                    safe=False)
                resp['token'] = None
                resp["Access-Control-Expose-Headers"] = "token"
                return resp
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 注册
def register(request):
    if request.method == "POST":
        user = json.loads(request.body)
        if user.get('telephone') and user.get('password') and user.get('name') and user.get('register_time'):
            res = newPerson(user)
            if not isinstance(res, dict):
                if res.id:
                    return JsonResponse({"status_code": "10001", "status_text": "注册成功"}, safe=False)
                else:
                    return JsonResponse({"status_code": "40004", "status_text": "系统错误"}, safe=False)
            else:
                return JsonResponse(res, safe=False)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
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
                        return JsonResponse({"status_code": "10014", "status_text": "更新成功"})
                    else:
                        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            except Exception as ex:
                print('个人信息改查错误')
                print(ex)
                return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
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
                for img in resp:
                    if img['type'] == 'dynamic':
                        i = list(smodels.DynamicImg.objects.filter(dynamic_id=img['id']).values('url'))
                        img['imgs'] = i
                    elif img['type'] == 'dairy':
                        i = list(smodels.DairyImg.objects.filter(dairy_id=img['id']).values('url'))
                        img['imgs'] = i
                    elif img['type'] == 'test':
                        i = list(smodels.TestImg.objects.filter(test_id=img['id']).values('url'))
                        img['imgs'] = i
                    else:
                        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
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
                mydairy = list(smodels.Dairy.objects.filter(user_id=user_id).values()[a:b])
                mydynamic = list(smodels.Dynamic.objects.filter(user_id=user_id).values()[a:b])
                mytest = list(smodels.Test.objects.filter(user_id=user_id).values()[a:b])
                for t in mytest:
                    ts = list(smodels.TestSubtitle.objects.filter(main_id=t['id']).values())
                    t['subtitle'] = ts
                res += mydairy
                res += mydynamic
                res += mytest
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
                resp = list(reversed(sorted(res, key=operator.itemgetter('date'))))[:10]
                for c in resp:
                    u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                    'icon_id').first()
                    ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                    c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                for img in resp:
                    if img['type'] == 'dynamic':
                        i = list(smodels.DynamicImg.objects.filter(dynamic_id=img['id']).values('url'))
                        img['imgs'] = i
                    elif img['type'] == 'dairy':
                        i = list(smodels.DairyImg.objects.filter(dairy_id=img['id']).values('url'))
                        img['imgs'] = i
                    elif img['type'] == 'test':
                        i = list(smodels.TestImg.objects.filter(test_id=img['id']).values('url'))
                        img['imgs'] = i
                    else:
                        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
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
                i = list(smodels.DynamicImg.objects.filter(dynamic_id=id).values('url'))
                res['imgs'] = i
                smodels.Dynamic.objects.filter(id=id).update(click=F('click') + 1)
            elif type == 'dairy':
                res = smodels.Dairy.objects.filter(id=id).values().first()
                i = list(smodels.DairyImg.objects.filter(dairy_id=id).values('url'))
                res['imgs'] = i
                smodels.Dairy.objects.filter(id=id).update(click=F('click') + 1)
            elif type == 'test':
                res = smodels.Test.objects.filter(id=id).values().first()
                i = list(smodels.TestImg.objects.filter(test_id=id).values('url'))
                res['imgs'] = i
                smodels.Test.objects.filter(id=id).update(click=F('click') + 1)
                ts = list(smodels.TestSubtitle.objects.filter(main_id=res['id']).values())
                res['subtitle'] = ts
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            u = models.UserInfo.objects.filter(user_id=res['user_id']).values('name',
                                                                            'icon_id').first()
            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
            res['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
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
                    if obtain.get('content') and obtain.get('type') and obtain.get('id') and obtain.get(
                            'user_id') and obtain.get('date'):
                        if obtain['type'] == 'dynamic':
                            obtain['Dynamic_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DynamicCom.objects.create(**obtain)
                            if res.id:
                                smodels.Dynamic.objects.filter(id=obtain['Dynamic_id']).update(com=F('com') + 1)
                        elif obtain['type'] == 'dairy':
                            obtain['Dairy_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DairyCom.objects.create(**obtain)
                            if res.id:
                                smodels.Dairy.objects.filter(id=obtain['Dairy_id']).update(com=F('com') + 1)
                        elif obtain['type'] == 'test':
                            obtain['Test_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.TestCom.objects.create(**obtain)
                            if res.id:
                                smodels.Test.objects.filter(id=obtain['Test_id']).update(com=F('com') + 1)
                        elif obtain['type'] == 'commodity':
                            obtain['commodity_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = semodels.CommodityCom.objects.create(**obtain)
                            if res.id:
                                semodels.Commodity.objects.filter(id=obtain['commodity_id']).update(com=F('com') + 1)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res.id:
                            models.UserInfo.objects.filter(user_id=obtain['user_id']).update(com=F('com') + 1)
                            return JsonResponse({"status_code": "10021", "status_text": "评论成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 删除评论
                elif obtain['method'] == 'del':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id'):
                        if obtain['type'] == 'dynamic':
                            res = smodels.DynamicCom.objects.filter(Dynamic_id=obtain['id'],user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Dynamic.objects.filter(id=obtain['id']).update(com=F('com') - 1)
                        elif obtain['type'] == 'dairy':
                            res = smodels.DairyCom.objects.filter(Dairy_id=obtain['id'],user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Dairy.objects.filter(id=obtain['id']).update(com=F('com') - 1)
                        elif obtain['type'] == 'test':
                            res = smodels.TestCom.objects.filter(Test_id=obtain['id'],user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Test.objects.filter(id=obtain['id']).update(com=F('com') - 1)
                        elif obtain['type'] == 'commodity':
                            res = semodels.CommodityCom.objects.filter(commodity_id=obtain['id'],user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                semodels.Commodity.objects.filter(id=obtain['id']).update(com=F('com') - 1)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res[0] == 1:
                            models.UserInfo.objects.filter(user_id=obtain['user_id']).update(com=F('com') - 1)
                            return JsonResponse({"status_code": "10010", "status_text": "删除成功"})
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
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                            'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'dairy':
                                        com = list(smodels.DairyCom.objects.filter(Dairy_id=i['id']).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                            'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'test':
                                        com = smodels.TestCom.objects.filter(Test_id=i['id']).values()
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                            'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    elif i['type'] == 'commodity':
                                        com = list(semodels.CommodityCom.objects.filter(commodity_id=i['id']).values())
                                        for c in com:
                                            u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                            'icon_id').first()
                                            ui = models.Icon.objects.filter(id=u['icon_id']).values('icon_url').first()
                                            c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                            resp.append(c)
                                    else:
                                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            return JsonResponse(resp, safe=False)
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
                            if res.id:
                                smodels.Dynamic.objects.filter(id=obtain['Dynamic_id']).update(fbs=F('fbs') + 1)
                        elif obtain['type'] == 'dairy':
                            obtain['Dairy_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DairyFbs.objects.create(**obtain)
                            if res.id:
                                smodels.Dairy.objects.filter(id=obtain['Dairy_id']).update(fbs=F('fbs') + 1)
                        elif obtain['type'] == 'test':
                            obtain['Test_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.TestFbs.objects.create(**obtain)
                            if res.id:
                                smodels.Test.objects.filter(id=obtain['Test_id']).update(fbs=F('fbs') + 1)
                        elif obtain['type'] == 'commodity':
                            obtain['commodity_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = semodels.CommodityFbs.objects.create(**obtain)
                            if res.id:
                                semodels.Commodity.objects.filter(id=obtain['commodity_id']).update(fbs=F('fbs') + 1)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res.id:
                            models.UserInfo.objects.filter(user_id=obtain['user_id']).update(fbs=F('fbs') + 1)
                            return JsonResponse({"status_code": "10018", "status_text": "赞成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                # 删除点赞
                elif obtain['method'] == 'del':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id'):
                        if obtain['type'] == 'dynamic':
                            res = smodels.DynamicFbs.objects.filter(Dynamic_id=obtain['id'],
                                                                    user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Dynamic.objects.filter(id=obtain['id']).update(fbs=F('fbs') - 1)
                        elif obtain['type'] == 'dairy':
                            res = smodels.DairyFbs.objects.filter(Dairy_id=obtain['id'],
                                                                  user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Dairy.objects.filter(id=obtain['id']).update(fbs=F('fbs') - 1)
                        elif obtain['type'] == 'test':
                            res = smodels.TestFbs.objects.filter(Test_id=obtain['id'],
                                                                 user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Test.objects.filter(id=obtain['id']).update(fbs=F('fbs') - 1)
                        elif obtain['type'] == 'commodity':
                            res = semodels.CommodityFbs.objects.filter(commodity_id=obtain['id'],
                                                                       user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                semodels.Commodity.objects.filter(id=obtain['id']).update(fbs=F('fbs') - 1)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res[0] == 1:
                            models.UserInfo.objects.filter(user_id=obtain['user_id']).update(fbs=F('fbs') - 1)
                            return JsonResponse({"status_code": "10010", "status_text": "删除成功"})
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
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10019'
                                                c['status_text'] = '已赞'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10020","status_text":"未赞"})
                                    elif i['type'] == 'dairy':
                                        if i.get('id'):
                                            i['Dairy_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(smodels.DairyFbs.objects.filter(**i).values())
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10019'
                                                c['status_text'] = '已赞'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10020","status_text":"未赞"})
                                    elif i['type'] == 'test':
                                        if i.get('id'):
                                            i['Test_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = smodels.TestFbs.objects.filter(**i).values()
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10019'
                                                c['status_text'] = '已赞'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10020","status_text":"未赞"})
                                    elif i['type'] == 'commodity':
                                        if i.get('id'):
                                            i['commodity_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(semodels.CommodityFbs.objects.filter(**i).values())
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10019'
                                                c['status_text'] = '已赞'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10020","status_text":"未赞"})
                                    else:
                                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            if not resp:
                                return JsonResponse([{"status_code": "10020", "status_text": "未赞"}],safe=False)
                            return JsonResponse(resp, safe=False)
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
                            if res.id:
                                smodels.Dynamic.objects.filter(id=obtain['Dynamic_id']).update(cols=F('cols') + 1)
                        elif obtain['type'] == 'dairy':
                            obtain['Dairy_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.DairyCol.objects.create(**obtain)
                            if res.id:
                                smodels.Dairy.objects.filter(id=obtain['Dairy_id']).update(cols=F('cols') + 1)
                        elif obtain['type'] == 'test':
                            obtain['Test_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = smodels.TestCol.objects.create(**obtain)
                            if res.id:
                                smodels.Test.objects.filter(id=obtain['Test_id']).update(cols=F('cols') + 1)
                        elif obtain['type'] == 'commodity':
                            obtain['commodity_id'] = obtain['id']
                            del obtain['id']
                            del obtain['type']
                            del obtain['method']
                            res = semodels.CommodityCol.objects.create(**obtain)
                            if res.id:
                                semodels.Commodity.objects.filter(id=obtain['commodity_id']).update(cols=F('cols') + 1)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res.id:
                            models.UserInfo.objects.filter(user_id=obtain['user_id']).update(cols=F('cols') + 1)
                            return JsonResponse({"status_code": "10015", "status_text": "收藏成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                # 删除收藏
                elif obtain['method'] == 'del':
                    if obtain.get('type') and obtain.get('id') and obtain.get('user_id'):
                        if obtain['type'] == 'dynamic':
                            res = smodels.DynamicCol.objects.filter(Dynamic_id=obtain['id'],
                                                                    user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Dynamic.objects.filter(id=obtain['id']).update(cols=F('cols') - 1)
                        elif obtain['type'] == 'dairy':
                            res = smodels.DairyCol.objects.filter(Dairy_id=obtain['id'],
                                                                  user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Dairy.objects.filter(id=obtain['id']).update(cols=F('cols') - 1)
                        elif obtain['type'] == 'test':
                            res = smodels.TestCol.objects.filter(Test_id=obtain['id'],
                                                                 user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                smodels.Test.objects.filter(id=obtain['id']).update(cols=F('cols') - 1)
                        elif obtain['type'] == 'commodity':
                            res = semodels.CommodityCol.objects.filter(commodity_id=obtain['id'],
                                                                       user_id=obtain['user_id']).delete()
                            if res[0] == 1:
                                semodels.Commodity.objects.filter(id=obtain['id']).update(cols=F('cols') - 1)
                        else:
                            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                        if res[0] == 1:
                            models.UserInfo.objects.filter(user_id=obtain['user_id']).update(cols=F('cols') - 1)
                            return JsonResponse({"status_code": "10010", "status_text": "删除成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
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
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                info = smodels.Dynamic.objects.filter(
                                                    id=c['Dynamic_id']).values().first()
                                                c['colInfo'] = info
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10016'
                                                c['status_text'] = '已收藏'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10017","status_text":"未收藏"})
                                    elif i['type'] == 'dairy':
                                        if i.get('id'):
                                            i['Dairy_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(smodels.DairyCol.objects.filter(**i).values())
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                info = smodels.Dairy.objects.filter(
                                                    id=c['Dairy_id']).values().first()
                                                c['colInfo'] = info
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10016'
                                                c['status_text'] = '已收藏'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10017","status_text":"未收藏"})
                                    elif i['type'] == 'test':
                                        if i.get('id'):
                                            i['Test_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = smodels.TestCol.objects.filter(**i).values()
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                info = smodels.Test.objects.filter(
                                                    id=c['Test_id']).values().first()
                                                c['colInfo'] = info
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['status_code'] = '10016'
                                                c['status_text'] = '已收藏'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code":"10017","status_text":"未收藏"})
                                    elif i['type'] == 'commodity':
                                        if i.get('id'):
                                            i['commodity_id'] = i['id']
                                            del i['id']
                                        del i['type']
                                        com = list(semodels.CommodityCol.objects.filter(**i).values())
                                        if com:
                                            for c in com:
                                                u = models.UserInfo.objects.filter(user_id=c['user_id']).values('name',
                                                                                                                'icon_id').first()
                                                ui = models.Icon.objects.filter(id=u['icon_id']).values(
                                                    'icon_url').first()
                                                info = semodels.Commodity.objects.filter(
                                                    id=c['commodity_id']).values().first()
                                                c['userInfo'] = {'name': u['name'], 'icon': ui['icon_url']}
                                                c['colInfo'] = info
                                                c['status_code'] = '10016'
                                                c['status_text'] = '已收藏'
                                                resp.append(c)
                                        else:
                                            resp.append({"status_code": "10017", "status_text": "未收藏"})
                                    else:
                                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            if not resp:
                                return JsonResponse([{"status_code": "10017", "status_text": "未收藏"}],safe=False)
                            return JsonResponse(resp, safe=False)
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
                        if obtain['concern_id'] == obtain['follower_id']:
                            return JsonResponse({"status_code":"10022","status_text":"不能关注自己"})
                        else:
                            del obtain['method']
                            res = models.Followers.objects.create(**obtain)
                            if res.id:
                                models.UserInfo.objects.filter(user_id=obtain['follower_id']).update(
                                    follow=F('follow') + 1)
                                models.UserInfo.objects.filter(user_id=obtain['concern_id']).update(fans=F('fans') + 1)
                                return JsonResponse({"status_code": "10009", "status_text": "关注成功"})
                            else:
                                return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                # 删除关注
                elif obtain['method'] == 'del':
                    if obtain.get('concern_id') and obtain.get('follower_id'):
                        del obtain['method']
                        res = models.Followers.objects.filter(**obtain).delete()
                        if res[0] == 1:
                            models.UserInfo.objects.filter(user_id=obtain['follower_id']).update(follow=F('follow') - 1)
                            models.UserInfo.objects.filter(user_id=obtain['concern_id']).update(fans=F('fans') - 1)
                            return JsonResponse({"status_code": "10010", "status_text": "删除成功"})
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
                        if res:
                            for c in res:
                                concern = models.UserInfo.objects.filter(user_id=c['concern_id']).values('name',
                                                                                                         'icon_id').first()
                                concern_i = models.Icon.objects.filter(id=concern['icon_id']).values('icon_url').first()
                                follower = models.UserInfo.objects.filter(user_id=c['follower_id']).values('name',
                                                                                                           'icon_id').first()
                                follower_i = models.Icon.objects.filter(id=concern['icon_id']).values(
                                    'icon_url').first()
                                c['concernInfo'] = {'name': concern['name'], 'icon': concern_i['icon_url']}
                                c['followerInfo'] = {'name': follower['name'], 'icon': follower_i['icon_url']}
                                c['status_code'] = '10011'
                                c['status_text'] = '已关注'
                                resp.append(c)
                        else:
                            return JsonResponse([{"status_code":"10012","status_text":"未关注"}],safe=False)
                        return JsonResponse(resp, safe=False)
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


# 七牛云token
def qiniuToken(request):
    from qiniu import Auth
    if request.method == 'POST':
        obtain = json.loads(request.body)
        try:
            if obtain.get('method'):
                # 需要填写你的 Access Key 和 Secret Key
                access_key = 'vp2ePBMNY-lgx6B6Rfh34jUoyjGwz8tJjvqdNlOC'
                secret_key = 'mHtY1slsiozUJ_QUif9qC1QxR9mqqxguu10sOJFf'
                # 构建鉴权对象
                q = Auth(access_key, secret_key)
                # 要上传的空间
                bucket_name = 'rainbow'
                domain = 'http://por6yfn25.bkt.clouddn.com'
                # 上传头像
                if obtain['method'] == 'icon' and obtain.get('iconname'):
                    # 上传到七牛后保存的文件名
                    filename = str(uuid.uuid4()) + '.' + obtain['iconname'].split('.')[1]
                    # 生成上传 Token，可以指定过期时间等
                    token = q.upload_token(bucket_name, filename, 3600)
                    return JsonResponse({"status_code":"20000","status_text":"请求成功", "qiniu_token": token, "filename": filename, "domain": domain})
                elif obtain['method'] == 'sharing' and obtain.get('name'):
                    file = []
                    for i in obtain['name']:
                        filename = str(uuid.uuid4()) + '.' + i.split('.')[1]
                        token = q.upload_token(bucket_name, filename, 3600)
                        file.append({"filename":filename, "token":token})
                    return JsonResponse(
                        {"status_code": "20000", "status_text": "请求成功", "file":file,"domain": domain})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('七牛云token错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})


# 保存图片
def imgSave(request):
    if request.method == 'POST':
        obtain = json.loads(request.body)
        try:
            if obtain.get('type'):
                if obtain['type'] == 'dynamic':
                    if obtain.get('id') and obtain.get('url'):
                        newImg = {"url":obtain['url'],"dynamic_id":obtain['id']}
                        res = smodels.DynamicImg.objects.create(**newImg)
                        if res.id:
                            return JsonResponse({"status_code":"10023","status_text":"保存成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                elif obtain['type'] == 'dairy':
                    if obtain.get('id') and obtain.get('url'):
                        newImg = {"url":obtain['url'],"dairy_id":obtain['id']}
                        res = smodels.DairyImg.objects.create(**newImg)
                        if res.id:
                            return JsonResponse({"status_code":"10023","status_text":"保存成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                elif obtain['type'] == 'test':
                    if obtain.get('id') and obtain.get('url'):
                        newImg = {"url":obtain['url'],"test_id":obtain['id']}
                        res = smodels.TestImg.objects.create(**newImg)
                        if res.id:
                            return JsonResponse({"status_code":"10023","status_text":"保存成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                elif obtain['type'] == 'commodity':
                    if obtain.get('id') and obtain.get('url'):
                        newImg = {"url":obtain['url'],"commodity_id":obtain['id']}
                        res = semodels.CommodityImg.objects.create(**newImg)
                        if res.id:
                            return JsonResponse({"status_code":"10023","status_text":"保存成功"})
                        else:
                            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
                    else:
                        return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                else:
                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
            else:
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
        except Exception as ex:
            print('保存图片错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})
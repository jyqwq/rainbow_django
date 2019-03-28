from django.http import HttpResponse, JsonResponse
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
            if obtain.get('type'):
                res = None
                print(obtain['type'])
                if obtain['type'] == 'dynamic':
                    if obtain.get('content') and obtain.get('tags') and obtain.get('date') and obtain.get('user_id'):
                        del obtain['type']
                        res = models.Dynamic.objects.create(**obtain)
                elif obtain['type'] == 'dairy':
                    if obtain.get('title') and obtain.get('content') and obtain.get('tags') and obtain.get('date') and obtain.get('user_id'):
                        del obtain['type']
                        res = models.Dairy.objects.create(**obtain)
                elif obtain['type'] == 'test':
                    if obtain.get('title') and obtain.get('content') and obtain.get('tags') and obtain.get('date') and obtain.get('user_id') and obtain.get('subtitle'):
                        sub = obtain['subtitle']
                        del obtain['subtitle']
                        del obtain['type']
                        res = models.Test.objects.create(**obtain)
                        print(res)
                        for s in sub:
                            if s.get('title') and s.get('content'):
                                s['main_id'] = res.id
                                r = models.TestSubtitle.objects.create(**s)
                                if r.id:
                                    pass
                                else:
                                    return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})
                            else:
                                return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
                else:
                    return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
                if res.id:
                    return JsonResponse({"status_code": "10008", "status_text": "发布成功", "id": int(res.id)})
                else:
                    return JsonResponse({"status_code":"40005","status_text":"数据格式不合法"})
        except Exception as ex:
            print('分享发布错误')
            print(ex)
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40000", "status_text": "请求方法不合法"})
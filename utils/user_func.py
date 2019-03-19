from user import models
from werkzeug.security import generate_password_hash, check_password_hash


# 登录方法
def online(user):
    rr = models.User.objects.filter(telephone=user['telephone']).values()

    if len(rr):
        aa = list(rr)[0]
        if aa['password']:
            if (check_password_hash(aa['password'], user['password'])):
                uu = models.UserInfo.objects.filter(user_id=aa['id']).values()
                return {"status_code":"10003","status_text":"登录成功",'id':aa['id'],'userInfo':list(uu)}
            else:
                return {"status_code": "10005", "status_text": "密码错误"}
        else:
            return {"status_code": "40004", "status_text": "系统错误"}
    else:
        return {"status_code": "10004", "status_text": "该用户不存在"}


# 注册方法
def newPerson(user):
    # uu = list(models.UserInfo.objects.filter(name='测试').values())
    # print(uu)
    try:
        # 查找昵称
        nn = models.UserInfo.objects.filter(name=user['name']).values()
        if len(nn):
            return {"status_code": "10000", "status_text": "用户名已经存在"}
        # 查找手机号
        rr = models.User.objects.filter(telephone=user['telephone']).values()
        if len(rr):
            return {"status_code": "10002", "status_text": "用户已经存在"}
        # 加密
        pf = generate_password_hash(user['password'], method='pbkdf2:sha1:1001', salt_length=8)
        newUser = {
            "telephone": user['telephone'],
            "password": pf,
            "register_time": user['register_time']
        }
        # 注册信息写入数据库User表
        res = models.User.objects.create(**newUser)
        # 找到刚写入的用户id
        newUserInfo = {
            "name": user['name'],
            "user_id": res.id
        }
        # 生成用户信息
        p = models.UserInfo.objects.create(**newUserInfo)
        return res
    except Exception as ex:
        print('注册方法错误信息:')
        print(ex)
        return {"status_code": "40004", "status_text": "系统错误"}


# 修改密码
def newPwd():
    pass


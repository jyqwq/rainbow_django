from django.db import models


# Create your models here.

# 用户表
class User(models.Model):
    telephone = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    register_time = models.CharField(max_length=255)


# 性别表
class Sex(models.Model):
    sex = models.CharField(max_length=50)


# 头像表
class Icon(models.Model):
    icon_url = models.CharField(max_length=254)


# 肤质表
class Skin(models.Model):
    skin = models.CharField(max_length=254)


# 关注表
class Followers(models.Model):
    follower = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE, default=1)
    concern = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE, default=1)
    date = models.CharField(max_length=255)


# 用户信息表
class UserInfo(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    autograph = models.CharField(max_length=255,default='这个人没有填简介啊~~~')
    birth = models.DateField(null=True)
    sex = models.ForeignKey(to='Sex', to_field='id', on_delete=models.CASCADE, default=1)
    icon = models.ForeignKey(to='Icon', to_field='id', on_delete=models.CASCADE, default=1)
    skin = models.ForeignKey(to='Skin', to_field='id', on_delete=models.CASCADE, default=1)
    fans = models.IntegerField(default=0)
    follow = models.IntegerField(default=0)
    fbs = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)
    com = models.IntegerField(default=0)


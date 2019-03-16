from django.db import models

# Create your models here.

# 品种
class Category(models.Model):
    Category = models.CharField(max_length=50)


# 产品
class Commodity(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    component = models.CharField(max_length=255)
    Effect = models.CharField(max_length=255)
    adaptability = models.ManyToManyField('user.Skin')
    category = models.ForeignKey(to='Category', to_field='id', on_delete=models.CASCADE)
    capacity = models.CharField(max_length=50)
    security = models.IntegerField()
    overdue = models.CharField(max_length=50)
    date = models.CharField(max_length=255)
    click = models.IntegerField(default=0)
    fbs = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)
    com = models.IntegerField(default=0)


# 产品图片
class CommodityImg(models.Model):
    url = models.CharField(max_length=255)
    commodity = models.ForeignKey(to='Commodity', to_field='id', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True)


# 产品点赞
class CommodityFbs(models.Model):
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    commodity = models.ForeignKey(to='Commodity', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 产品收藏
class CommodityCol(models.Model):
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    commodity = models.ForeignKey(to='Commodity', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 产品评论
class CommodityCom(models.Model):
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE)
    commodity = models.ForeignKey(to='Commodity', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.CharField(max_length=255)


# 搜索关键字
class SearchKey(models.Model):
    user = models.ForeignKey(to='user.User', to_field='id', on_delete=models.CASCADE, default=0)
    content = models.CharField(max_length=255)
    date = models.CharField(max_length=255)

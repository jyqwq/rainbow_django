from django.db import models

# Create your models here.

# 心情表
class Dynamic(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    click = models.IntegerField(default=0)
    fbs = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)
    com = models.IntegerField(default=0)


# 日记表
class Dairy(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    click = models.IntegerField(default=0)
    fbs = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)
    com = models.IntegerField(default=0)


# 测评表
class Test(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    click = models.IntegerField(default=0)
    fbs = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)
    com = models.IntegerField(default=0)


# 测评附表
class TestSubtitle(models.Model):
    main = models.ForeignKey(to='Test',to_field='id',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

# 心情图片
class DynamicImg(models.Model):
    url = models.CharField(max_length=255)
    dynamic = models.ForeignKey(to='Dynamic', to_field='id', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True)


# 日记图片
class DairyImg(models.Model):
    url = models.CharField(max_length=255)
    dairy = models.ForeignKey(to='Dairy', to_field='id', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True)


# 测评图片
class TestImg(models.Model):
    url = models.CharField(max_length=255)
    test = models.ForeignKey(to='Test', to_field='id', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True)

# 心情点赞
class DynamicFbs(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Dynamic = models.ForeignKey(to='Dynamic', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 日记点赞
class DairyFbs(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Dairy = models.ForeignKey(to='Dairy', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 测评点赞
class TestFbs(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Test = models.ForeignKey(to='Test', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 心情收藏
class DynamicCol(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Dynamic = models.ForeignKey(to='Dynamic', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 日记收藏
class DairyCol(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Dairy = models.ForeignKey(to='Dairy', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 测评收藏
class TestCol(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Test = models.ForeignKey(to='Test', to_field='id', on_delete=models.CASCADE)
    date = models.CharField(max_length=255)


# 心情评论
class DynamicCom(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Dynamic = models.ForeignKey(to='Dynamic', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.CharField(max_length=255)


# 日记评论
class DairyCom(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Dairy = models.ForeignKey(to='Dairy', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.CharField(max_length=255)


# 测评评论
class TestCom(models.Model):
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)
    Test = models.ForeignKey(to='Test', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
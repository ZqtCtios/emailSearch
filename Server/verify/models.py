from django.db import models

# Create your models here.
class UserMessage(models.Model):
    userId=models.CharField(max_length=50,default="",verbose_name="账号")
    userName=models.CharField(max_length=50,verbose_name="用户名")
    password=models.CharField(max_length=50,verbose_name="密码")
    date=models.DateField(verbose_name="注册日期")
    isVerified=models.IntegerField(verbose_name="激活状态")
    remainder=models.IntegerField(verbose_name="剩余天数")
    loginFlag=models.IntegerField(verbose_name="登陆状态")
    class Meta:
        verbose_name="用户信息"

# django的ORM数据模型；直接操作数据库

from django.db import models


# Create your models here.
# 用户信息表
class UserInFo(models.Model):
    id = models.AutoField('用户表主键', primary_key=True)
    username = models.CharField('用户姓名', max_length=25, null=False)
    create = models.DateTimeField('用户创建的时间', auto_now_add=True)

    # 元类信息；修改表名
    class Meta:
        db_table = "userinfo"


# 汽车信息表
class CarInfo(models.Model):
    id = models.AutoField('车辆编号', primary_key=True)
    carpinpai = models.CharField('车辆品牌', max_length=125, null=False)
    carname = models.CharField('车辆名字', max_length=125, null=False)
    carprice = models.CharField('车辆价格', max_length=125, null=True)
    carimage = models.CharField('车辆图片',  max_length=355,  null=True)

    #  元类信息，修改表名
    class Meta:
        db_table = 'carinfo'

"""
    配置接口路由
"""

from django.urls import path
from . import views

urlpatterns = {
    path("register", views.registerUser),  # 注册
    path("getCar",  views.getCar),  # 获取车的数据
    path("weixinPay", views.weixinPay)
}

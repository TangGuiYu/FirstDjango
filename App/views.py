import json
import random
import time
import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.datetime_safe import strftime
from weixin import Weixin

from .models import *
from django.http import JsonResponse

# Create your views here.

"""
    逻辑层
"""


#  注册
def registerUser(request):
    # 接受前端传来的注册信息参数
    # name = request.POST.get("name", "")  # 用户姓名
    try:
        if request.method == "POST":
            try:
                postboy = request.body
                jsonResult = json.loads(postboy)
                # 添加数据奥数据库
                userinsert = UserInFo(username=jsonResult['name'])
                # # 提交执行
                userinsert.save()

                return JsonResponse(
                    {
                        'code': 1,
                        'msg': '接受POST到请求，注册成功' + str(jsonResult['name'])
                    }
                )
            except Exception as err:
                return JsonResponse(
                    {
                        'code': 0,
                        'msg': err
                    }
                )
        else:
            return JsonResponse(
                {
                    'code': 1,
                    'msg': '接受Get到请求'
                }
            )
    except Exception as e:
        return JsonResponse(
            {
                'code': 0,
                'msg': e
            }
        )


# 汽车数据;分页
def getCar(request):
    try:
        # 获取页面数据
        postbody = request.body
        jsonResult = json.loads(postbody)

        # 获取页码数据
        nextPage = jsonResult['currentPage']

        # 所有车辆的数据
        allCar = CarInfo.objects.all().values()

        # 分页；每页十条数据
        p = Paginator(allCar, 10)  # 使用Paginator分页器，讲所有数据进行分页，每页10条数据

        # 获取当前页码的数据
        pagelist = p.get_page(nextPage)

        # 返回数据
        listSQL = list(pagelist)
        return JsonResponse(
            {
                'code': 1,
                'msg': '读取数据成功',
                'data': listSQL,
                'pageCount': p.num_pages,
                'currentPage': nextPage
            }
        )
    except Exception as e:
        return JsonResponse(
            {
                'code': 0,
                'msg': e
            }
        )


# 微信支付

def weixinPay(request):
    WEIXIN_APP_ID = 'wx72226564d6a93c08'
    WEIXIN_MCH_KEY = 'Yuanlong202188888888888888888888'
    WEIXIN_MCH_ID = '1611227606'
    WEIXIN_NOTIFY_URL = 'www.yuanlong.xyz'

    config = dict(
        WEIXIN_APP_ID=WEIXIN_APP_ID,
        WEIXIN_MCH_KEY=WEIXIN_MCH_KEY,  # 密钥
        WEIXIN_MCH_ID=WEIXIN_MCH_ID,
        WEIXIN_NOTIFY_URL=WEIXIN_NOTIFY_URL,
    )
    weixin = Weixin(config)
    # 设置过期时间,当前是下单后30分钟关闭交易,设置订单提示信息.
    wx_time_expire = (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime('%Y%m%d%H%M%S')
    # 生成9位随机订单号
    noOrer = ""
    for i in range(6):
        noOrer += str(random.randint(0, 9))

    wei = weixin.unified_order(
        out_trade_no="YYYY" + noOrer,  # 订单id
        body="2022款 iPhone Pro Max 256G 星光自",#  描述
        total_fee=1,  # 这个是0.01
        trade_type='JSAPI',  # JSAPI微信支付
        time_expire=wx_time_expire,
        product_id='shangpinid',  # 二维码中包含的商品ID
        openid='o0oFy5ed6jJK2I114s16YkBNTAyk',  # 这个是关注我们公众号的用户的openid,不同的key得到的openid是不一样的
    )

    sing_data = {
        "appId": weixin.app_id,  # 公众号名称，由商户传入
        "timeStamp": str(int(time.time())),  # 时间戳，自1970年以来的秒数
        "nonceStr": weixin.nonce_str,  # 随机串
        "package": f"prepay_id={wei.get('prepay_id')}",
        "signType": "MD5",  # 微信签名方式：
    }
    # weixin.sign(sing_data)这个是生产md5签名
    sing_data.setdefault('paySign', weixin.sign(sing_data))
    # sing_data这个字典,前端可以直接用,当参数直接携带传递给微信
    message = {
        'succeed': '支付请求成功',
        'message': sing_data
    }
    return JsonResponse(message)

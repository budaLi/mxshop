from django.db import models
#通过这种方式将重写的user类加载
from django.contrib.auth import get_user_model
from datetime import datetime
# Create your models here.
from goods.models import Goods
User=get_user_model()

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User,verbose_name=u'用户',on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,verbose_name=u'商品',on_delete=models.CASCADE)
    nums = models.IntegerField(default=0,verbose_name=u'购买数量')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='购物车'
        verbose_name_plural = verbose_name
        #相当于数据库中联合约束 购物车中可以有不同用户的不同商品信息 用这两个数据表示唯一 如果这两个数据和表中的数据一致就会被拒绝加入 只能增加购买数量
        unique_together = ('user','goods')

    def __str__(self):
        #返回购物车中商品名字和数量
        return "%s(%d)".format(self.goods.name,self.nums)

class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ('TRADE_SUCESS','成功'),
        ('TRADE_CLOSED','超时关闭'),
        ('WAIT_BUYER_PAY','交易创建'),
        ('TRADE_FINISHED','交易结束'),
        ('PAYING','待支付'),
    )
    user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30,null=True,blank=True,unique=True,verbose_name='订单号')
    trade_no = models.CharField(max_length=100,unique=True,null=True,blank=True,verbose_name='交易号')
    pay_status = models.CharField(choices=ORDER_STATUS,default='PAYING',max_length=30,verbose_name='订单状态')
    post_script = models.CharField(max_length=200,verbose_name='订单留言')
    order_mount = models.FloatField(default=0.0,verbose_name='订单金额')
    pay_time = models.DateTimeField(default=datetime.now,verbose_name='支付时间')

    #用户信息
    address = models.CharField(max_length=100,default='',verbose_name='收货地址')
    signer_name = models.CharField(max_length=20,default='',verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11,verbose_name='联系电话')

    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural= verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    #在这里可以通过 一个订单号得到该订单的全部商品信息 ？ 可以为什么在order字段设置
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods",on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品",on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
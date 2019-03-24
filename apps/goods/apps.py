from django.apps import AppConfig


class GoodsConfig(AppConfig):

    #此处直接写app名字就可以 不用apps.goods
    name = 'goods'

    #该字段可以使xadmin后台中每个app的名字显示为中文
    verbose_name = '商品管理'

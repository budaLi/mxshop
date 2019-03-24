from django.views.generic.base import View
from goods.models import Goods
import json

#此文件是用于直接返回json文件 以区别django-restfor
class GoodsListView(View):
    def get(self,request):
        """
        通过django的View实现商品列表页
        :param request:
        :return:
        """
        # json_list = []
        goods = Goods.objects.all()[10:]
        # for good in goods:
        #     json_dic={}
        #     json_dic['name']=good.name
        #     json_dic['category'] = good.category.name
        #     json_dic['market_price'] = good.market_price
        #     json_list.append(json_dic)

        #这种方法无法序列化 日期类型 图片类型等
        # from django.forms.models import  model_to_dict
        # for good in goods:
        #     json_dic=model_to_dict(good)
        #     json_list.append(json_dic)

        #同样存在问题
        # from django.core import serializers
        # for good in goods:
        #     json_dic=serializers.serialize('json',good)
        #     json_list.append(json_dic)

        from django.core import serializers
        json_data = serializers.serialize('json',goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse,JsonResponse

        #此处要注意要返回Json格式必须指定content_type
        #这种方式返回图片路径等给前端时无法正确传递资源
        # return HttpResponse(json.dumps(json_data),content_type='application/json')

        #In order to allow non-dict objects to be serialized set the safe parameter to False.
        #上述报错需要设置safe参数
        #坏处和上面一样 无法正确给前端传递图片等资源
        return JsonResponse(json_data,safe=False)

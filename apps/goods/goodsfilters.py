import django_filters
from .models import Goods
from django.db.models import Q

class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    #gt表示大于 gte大于等于 lt 小于 lte 小于等于
    pricemin = django_filters.NumberFilter(field_name='shop_price',lookup_expr='gt')
    pricemax = django_filters.NumberFilter(field_name='shop_price',lookup_expr='lt')
    # name = django_filters.CharFilter(field_name='name',lookup_expr='contains')  #如果加i则表示忽略大小写 不写lookup则表示完全匹配

    #这样可以使用自定义filter
    top_category = django_filters.NumberFilter(method='top_category_filter')

    #这些值是默认传递的
    def top_category_filter(self,queryset,name,value):
        #通过引入django的或函数 Q
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
    class Meta:
        model = Goods
        fields = ['pricemin' , 'pricemax']
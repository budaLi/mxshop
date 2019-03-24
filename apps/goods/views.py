from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins,generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.filters import SearchFilter,OrderingFilter
#使用django-filters进行过滤
from django_filters.rest_framework import DjangoFilterBackend

from .goodsfilters import GoodsFilter
# from rest_framework import status
#在这里表示当前路径下的
from .models import Goods,GoodsCategory

#导入序列化的对象
from .serializers import GoodsSerializer,CategorySerializer

# Create your views here.

# 第一种方式
# class GoodsListView(APIView):
#     """
#     List all goods
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[10:]
#         #many参数表示是多个对象 如果获取的结果是一个值就不需要指定
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)
#
#         def post(self,request,format=None):
#             serializer = GoodsSerilizer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_201_CREATED)
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#第二种方式
#这种方式比继承Apiview更方便
# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     """
#     商品列表页
#     """
#     #注意此处两个变量的书写方式为重写 名称不能变
#     queryset = Goods.objects.all()[10:]
#     serializer_class = GoodsSerializer
#     def get(self, request, *args,**kwargs):
#         return self.list(request,*args,**kwargs)

#第三种方式 比第二种更好 封装了分页功能 以及在图片文件前面加域名等
# class GoodPagination(PageNumberPagination):
#     page_size = 10
#     #可以指定每页取多少条数据 page_size=20
#     page_size_query_param = 'page_size'
#     page_query_param = 'p'
#     #指定每页能取得最大条
#     max_page_size = 100
#
# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodPagination


#第四种方式 viewset 他重写了as_view方法 让注册url更简单
class GoodPagination(PageNumberPagination):

    # 可以指定每页取多少条数据 page_size
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    #指定每页能取得最大条
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    List:
        商品列表页 分页 搜索 过滤 排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodPagination

    #第一种
    #drf的过滤 他会自动找上面queryset的函数执行 此处函数名不能变
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     #通过query_params.get方法获取前端的价格最小值 默认为0
    #     price_min = self.request.query_params.get('price_min',0)
    #     #注意次数字段名的写法 为models字段名+__gt
    #     queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset

    #第二种
    #使用django-filters进行过滤  在这里要注意 过滤和搜索不一样 这里要求完全等于才会有数据
    #这种写法无法满足模糊搜索
    #注意此处是元祖形式
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields= ('name','shop_price')

    #第三种
    #通过自己写filters实现过滤 和搜索
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = GoodsFilter

    # ^ 表示已某个字段开头  = 表示精确查找  @ 表示全文搜索 mysql  $表示正则搜索
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')

class CategoryListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    List:
        商品分类列表数据
    """
    #导航栏不需要分页功能  在这里要指定商品类别为1
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

    #上面的功能是返回商品分类的全部数据 还有一个需求是得到某个第一大分类的其余数据
    #在这里只需多继承一个类就可以实现  mixins.RetrieveModelMixin 如上所示  url会同时自动配置好
    #比如我们要获取全部goods信息  使用 goods/  获取某一类商品详情 goods/id
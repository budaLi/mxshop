from rest_framework import serializers
from .models import Goods,GoodsCategory

#第一种方式
# #这种方式类似于django中的form表单的作用
# class GoodsSerilizer(serializers.Serializer):
#
#     name = serializers.CharField(required=True)
#     click_num = serializers.IntegerField(default=0)
#     #这里序列化的图片路径为设置的媒体文件路径加上数据库中存储的文件路径
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         根据前端数据生成数据
#         :param validated_data:
#         :return:
#         """
#         return Goods.objects.create(**validated_data)


#第二种方式
class CategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化 第三级别
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化 第二级别
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    #在这里 一定要注意如果存在多个数据 要配置many=True
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

#类似于django中的modelform形式  注意此处继承的类不一样
class GoodsSerializer(serializers.ModelSerializer):

    #通过覆盖原有字段的方式 可以将外键序列化 如果不覆盖会将该字段显示为外键id
    category= CategorySerializer()
    class Meta:
        model = Goods
        fields = "__all__"
from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField  #富文本编辑器
# Create your models here.
class GoodsCategory(models.Model):
    """
    商品类别
    主要用于前端商品分类导航
    """
    # 二元元组中第一个元素是要存入数据库中的数据 第二个是在adm
    CATEGORY_TYPE = (
        (1,'一级类目'),
        (2,'二级类目'),
        (3,'三级类目')
    )

    #help_text可以用于生成文档
    name = models.CharField(default='',max_length=30,verbose_name='类别名',help_text='类别名')
    code = models.CharField(default='',max_length=30,verbose_name='类别编码',help_text='类别编码')
    desc = models.TextField(default='',verbose_name='类别描述',help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE,verbose_name='类目级别',help_text='类目级别')
    #related_name的作用  https://blog.csdn.net/hpu_yly_bj/article/details/78939748
    #django默认情况下每一个主表的对象都有一个是外键的属性，可以通过它查询到所有关于子表的信息，这个属性的名字就是子表的名称小写加上_set
    #比如有一个教师表和学生表 一个教师对应多个学生 查询某个教师对应的全部学生 teacher,.student_set.all()
    #当我们设置related_name时  就可以通过related_name的方式替换上述方式
    #当查询一个学生对应的教师信息时 可以通过student.teacher.xxx这种形式获取
    parent_category = models.ForeignKey('self',null=True,blank=True,verbose_name='父类目级别',help_text='父目录',
                                        related_name='sub_cat',on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False,verbose_name='是否导航',help_text='是否导航')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名 商家
    """
    category = models.ForeignKey(GoodsCategory,related_name='brands',null=True,blank=True,verbose_name='商品类目',on_delete=models.CASCADE)
    name = models.CharField(default='',max_length=30,verbose_name='品牌名',help_text='品牌名')
    desc = models.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name

class Goods(models.Model):
    """
    商品
    """
    #第一级商品类别 没有父目录 所以要设置为空
    category = models.ForeignKey(GoodsCategory, null=True,blank=True,verbose_name="商品类目",on_delete=models.CASCADE)

    #自动生成的id用于代码设计时作为主键 good_sn用于商家取货时
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, related_name='category',verbose_name="商品类目",on_delete=models.CASCADE)
    goods =models.ForeignKey(Goods, related_name='goods',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name="商品",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
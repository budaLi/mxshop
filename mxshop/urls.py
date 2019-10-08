"""mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url,include
import xadmin
from django.contrib import admin
#这两个设置是设置图片显示的
from mxshop.settings import MEDIA_ROOT
from django.views.static import serve

#导入drf
from rest_framework.documentation import include_docs_urls

#drf的登录验证
from rest_framework.authtoken import views
#jwt认证
from rest_framework_jwt.views import obtain_jwt_token
#这个是用来说明drf的重要性的
# from goods.view_base import GoodsListView
from goods.views import GoodsListViewSet,CategoryListViewSet


# goods_list = GoodsListViewSet.as_view({
#     'get':'list'
# })

#通过router避免上述方式 自动配置
from rest_framework.routers import DefaultRouter
route = DefaultRouter()
#配置goods的url
route.register(r'goods',GoodsListViewSet,base_name='goods')
#配置category的url
route.register(r'categorys',CategoryListViewSet,base_name='category')

urlpatterns = [

    # url(r'admin/', admin.site.urls),
    url(r'xadmin/',xadmin.site.urls),

    #drf登录需要的配置
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    #商品列表页 当使用routre时不需要配置
    # url(r'goods/$',goods_list,name='good-list'),
    url(r'^',include(route.urls)),


    #这里一定要注意 $符号一定要删除
    url(r'docs',include_docs_urls(title='慕课生鲜')),

    #drf自带的认证
    # url('api-token-auth/', views.obtain_auth_token)

    #jwt认证
    url('login/', obtain_jwt_token)
]

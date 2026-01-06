"""pyflowable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # django后台管理页面
    re_path(r'^admin/', admin.site.urls),
    # 根路径重定向
    path("", RedirectView.as_view(url='/login/', permanent=False), name='root-redirect'),
    # 登录按钮
    path("", include("rest_framework.urls")),
    # JWT Token
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # {"username":"","password":""}
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),  # {"refresh":"上面接口返回的refresh字段"}
    # 获取 OpenAPI 架构文件
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 可选的 Swagger UI 界面
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    # 可选的 ReDoc 界面
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

api_urlpatterns = [
    path('api/user/', include('user.urls'), name='user'),
    path('api/flowable/', include('flowable.urls'), name='flowable'),
]

urlpatterns = urlpatterns + api_urlpatterns

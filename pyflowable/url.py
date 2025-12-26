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
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.urls import router as user_router
from apps.flowable.urls import router as flowable_router

# 统一管理路径
main_router = DefaultRouter()
for prefix, viewset, basename in user_router.registry:
    main_router.register(f'user/{prefix}', viewset, basename=basename)
for prefix, viewset, basename in flowable_router.registry:
    main_router.register(f'flowable/{prefix}', viewset, basename=basename)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # 根路径重定向
    path("", RedirectView.as_view(url='/login/', permanent=False), name='root-redirect'),
    # 登录按钮
    path("", include("rest_framework.urls")),
    # API
    path('api/', include(main_router.urls)),  # 所有API都在api下

    # JWT Token
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # {"username":"","password":""}
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),  # {"refresh":"上面接口返回的refresh字段"}

]

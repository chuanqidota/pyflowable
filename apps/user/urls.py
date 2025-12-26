from django.urls import path
from rest_framework.routers import DefaultRouter

from user.api.login import ManualLoginView
from user.api.user import UserViewSet, GroupViewSet

app_name = 'user'

router = DefaultRouter()
router.registry("group", GroupViewSet, "group")  # 用户分组
router.registry("user", UserViewSet, "user")  # 用户

urlpatterns = [
    path('v1/manual-login', ManualLoginView.as_view(), name='manual-login'),  # 手动登陆
]

urlpatterns += router.urls

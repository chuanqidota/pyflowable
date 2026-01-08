from django.urls import path
from rest_framework.routers import DefaultRouter

from user.api.login import ManualLoginView
from user.api.user import UserViewSet, GroupViewSet, CreateGroupView, DeleteGroupView

app_name = 'user'

router = DefaultRouter()
router.register("v1/group", GroupViewSet, basename="group")  # 用户分组
router.register("v1/user", UserViewSet, basename="user")  # 用户

urlpatterns = [
    path('v1/manual-login', ManualLoginView.as_view(), name='manual-login'),  # 手动登陆
    path('v1/create-group', CreateGroupView.as_view(), name='create-group'),  # 创建用户分组在数据库和flowable
    path('v1/delete-group', DeleteGroupView.as_view(), name='delete-group'),  # 删除用户分组在数据库和flowable
]

urlpatterns += router.urls

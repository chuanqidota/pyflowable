from django.urls import path
from rest_framework.routers import DefaultRouter

from user.api.group import GroupViewSet
from user.api.login import ManualLoginView
from user.api.user import UserViewSet

app_name = 'user'

router = DefaultRouter()
router.registry("group", GroupViewSet, basename="user")
router.registry("user", UserViewSet, basename="user")

urlpatterns = [
    path('v1/manual-login', ManualLoginView.as_view(), name='manual-login'),
]

urlpatterns += router.urls

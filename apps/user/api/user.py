from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.mixins.login import LoginRequiredMixin
from user.models import User, Group
from user.serializers.group import GroupSerializer
from user.serializers.user import UserSerializer


class GroupViewSet(LoginRequiredMixin, ModelViewSet):
    """
        用户分组
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ["name", "alias"]
    filterset_fields = ["name", "alias"]
    ordering_fields = ["id", "created_at"]
    ordering = ["-id"]


class UserViewSet(LoginRequiredMixin, ModelViewSet):
    """
        用户信息
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["group__name", "username", "name", "email"]
    filterset_fields = ["is_active", "group__name", "username", "name", "email"]
    ordering_fields = ["id", "created_at"]
    ordering = ['-id']

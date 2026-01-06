from types import UnionType

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from user.mixins.login import LoginRequiredMixin
from user.models import User, Group
from user.serializers.group import GroupSerializer, GroupHasUserSerializer
from user.serializers.user import UserSerializer


@extend_schema_view(
    list=extend_schema(summary="用户分组列表", tags=['用户分组']),
    create=extend_schema(summary="用户分组创建", tags=['用户分组']),
    retrieve=extend_schema(summary="用户分组详情", tags=['用户分组']),
    update=extend_schema(summary="用户分组更新", tags=['用户分组']),
    partial_update=extend_schema(summary="用户分组部份更新", tags=['用户分组']),
    destroy=extend_schema(summary="用户分组删除", tags=['用户分组']),
)
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

    def get_serializer_class(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "user_list":
            return GroupHasUserSerializer
        return super().get_serializer_class()

    @extend_schema(parameters=[OpenApiParameter(name='serializer', enum=['user_list'])])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(summary="用户列表", tags=['用户']),
    create=extend_schema(summary="用户创建", tags=['用户']),
    retrieve=extend_schema(summary="用户详情", tags=['用户']),
    update=extend_schema(summary="用户更新", tags=['用户']),
    partial_update=extend_schema(summary="用户部份更新", tags=['用户']),
    destroy=extend_schema(summary="用户删除", tags=['用户']),
)
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

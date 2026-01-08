from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.mixins.login import LoginRequiredMixin
from user.models import User, Group
from user.serializers.group import GroupSerializer, GroupHasUserSerializer
from user.serializers.user import UserSerializer, CreateUserSerializer
from user.service.group import ActionGroup
from utils.response import SuccessResp


@extend_schema_view(
    list=extend_schema(summary="用户分组列表", tags=['用户分组']),
    create=extend_schema(summary="用户分组创建", tags=['用户分组']),
    retrieve=extend_schema(summary="用户分组详情", tags=['用户分组']),
    update=extend_schema(summary="用户分组更新", tags=['用户分组']),
    partial_update=extend_schema(summary="用户分组部份更新", tags=['用户分组']),
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

    @extend_schema(summary="用户分组删除", tags=['用户分组'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(summary="批量删除用户组", tags=['用户分组'],
                   parameters=[OpenApiParameter(name='id__in', description="英文逗号分割", required=True)])
    @action(methods=['delete'], detail=False, url_path='bulk-destroy')
    def bulk_destroy(self, request, *args, **kwargs):
        id__in = request.query_params.get("id__in")
        if id__in:
            queryset = self.get_queryset().filter(id__in=id__in.split(","))
            queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateGroupView(LoginRequiredMixin, APIView):
    """
        创建用户分组在数据库和flowable
    """

    @extend_schema(
        summary='创建用户分组在数据库和flowable',
        request=inline_serializer(
            name='CreateGroupRequestSerializer',
            fields={
                'name': serializers.CharField(help_text='组名称'),
                'alias': serializers.CharField(help_text='组ID'),
            }
        ),
        responses={
            200: inline_serializer(
                name='CreateSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["用户分组"]
    )
    def post(self, request):
        data = request.data
        name = data.get("name")
        alias = data.get("alias")
        ActionGroup().create_group(name, alias)
        return SuccessResp()


class DeleteGroupView(LoginRequiredMixin, APIView):
    """
        删除用户分组在数据库和flowable
    """

    @extend_schema(
        summary='删除用户分组在数据库和flowable',
        request=inline_serializer(
            name='DeleteGroupRequestSerializer',
            fields={
                'alias': serializers.CharField(help_text='组ID')
            }
        ),
        responses={
            200: inline_serializer(
                name='DeleteSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["用户分组"]
    )
    def delete(self, request):
        data = request.data
        alias = data.get("alias")
        ActionGroup().delete_group(alias)
        return SuccessResp()


@extend_schema_view(
    list=extend_schema(summary="用户列表", tags=['用户']),
    create=extend_schema(summary="用户创建", tags=['用户']),
    retrieve=extend_schema(summary="用户详情", tags=['用户']),
    update=extend_schema(summary="用户更新", tags=['用户']),
    partial_update=extend_schema(summary="用户部份更新", tags=['用户']),
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

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return super().get_serializer_class()

    @extend_schema(summary="用户删除", tags=['用户'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(summary="批量删除用户", tags=['用户'],
                   parameters=[OpenApiParameter(name='id__in', description="英文逗号分割", required=True)])
    @action(methods=['delete'], detail=False, url_path='bulk-destroy')
    def bulk_destroy(self, request, *args, **kwargs):
        id__in = request.query_params.get("id__in")
        if id__in:
            queryset = self.get_queryset().filter(id__in=id__in.split(","))
            queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

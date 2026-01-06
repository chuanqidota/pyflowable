from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from flowable.models.process import Process
from flowable.models.process_attr import ProcessAttr
from flowable.models.process_group import ProcessGroup
from flowable.serializers.process import ProcessSerializers, ProcessHasInstanceSerializers, ProcessHasAttrSerializers
from flowable.serializers.process_attr import ProcessAttrSerializers
from flowable.serializers.process_group import ProcessGroupSerializers
from user.mixins.login import LoginRequiredMixin


@extend_schema_view(
    list=extend_schema(summary="流程分组列表", tags=['流程分组管理']),
    create=extend_schema(summary="流程分组创建", tags=['流程分组管理']),
    retrieve=extend_schema(summary="流程分组详情", tags=['流程分组管理']),
    update=extend_schema(summary="流程分组更新", tags=['流程分组管理']),
    partial_update=extend_schema(summary="流程分组部份更新", tags=['流程分组管理']),
    destroy=extend_schema(summary="流程分组删除", tags=['流程分组管理']),
)
class ProcessGroupViewSet(LoginRequiredMixin, ModelViewSet):
    """
        流程分组
    """
    queryset = ProcessGroup.objects.all()
    serializer_class = ProcessGroupSerializers
    search_fields = ["name"]
    filterset_fields = ["name"]
    ordering_fields = ["id", "sort", "create_time"]
    ordering = ["-id"]


@extend_schema_view(
    list=extend_schema(summary="流程列表", tags=['流程管理']),
    create=extend_schema(summary="流程创建", tags=['流程管理']),
    retrieve=extend_schema(summary="流程详情", tags=['流程管理']),
    update=extend_schema(summary="流程更新", tags=['流程管理']),
    partial_update=extend_schema(summary="流程部份更新", tags=['流程管理']),
    destroy=extend_schema(summary="流程删除", tags=['流程管理']),
)
class ProcessViewSet(LoginRequiredMixin, ModelViewSet):
    """
        流程定义
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializers
    search_fields = ["name", "key"]
    filterset_fields = ["name", "group__name"]
    ordering_fields = ["id", "sort", "create_time"]
    ordering = ["-id"]

    def get_serializer_class(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "instance_list":
            return ProcessHasInstanceSerializers
        elif serializer == "attr_list":
            return ProcessHasAttrSerializers
        else:
            return super().get_serializer_class()

    @extend_schema(parameters=[OpenApiParameter(name='serializer', enum=['instance_list', 'attr_list'])])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(summary="流程属性列表", tags=['流程属性管理']),
    create=extend_schema(summary="流程属性创建", tags=['流程属性管理']),
    retrieve=extend_schema(summary="流程属性详情", tags=['流程属性管理']),
    update=extend_schema(summary="流程属性更新", tags=['流程属性管理']),
    partial_update=extend_schema(summary="流程属性部份更新", tags=['流程属性管理']),
    destroy=extend_schema(summary="流程属性删除", tags=['流程属性管理']),
)
class ProcessAttrViewSet(LoginRequiredMixin, ModelViewSet):
    """
        流程属性
    """
    queryset = ProcessAttr.objects.all()
    serializer_class = ProcessAttrSerializers
    search_fields = ["name", "code"]
    filterset_fields = ["name", "code", "process__name", "process__key"]
    ordering_fields = ["id", "create_time"]
    ordering = ["-id"]

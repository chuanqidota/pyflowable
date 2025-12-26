from rest_framework.viewsets import ModelViewSet

from flowable.models.process import Process
from flowable.models.process_attr import ProcessAttr
from flowable.models.process_group import ProcessGroup
from flowable.serializers.process import ProcessSerializers, ProcessHasInstanceSerializers, ProcessHasAttrSerializers
from flowable.serializers.process_attr import ProcessAttrSerializers
from flowable.serializers.process_group import ProcessGroupSerializers
from user.mixins.login import LoginRequiredMixin


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

from rest_framework.viewsets import ModelViewSet

from flowable.models.instance import Instance
from flowable.models.instance_task import InstanceTask
from flowable.serializers.instance import InstanceSerializers, InstanceHasAttrValueSerializers, \
    InstanceHasTaskSerializers
from flowable.serializers.instance_task import InstanceTaskSerializers, InstanceTaskHasGroupUserSerializers
from user.mixins.login import LoginRequiredMixin


class InstanceViewSet(LoginRequiredMixin, ModelViewSet):
    """
        实例信息
    """
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializers
    search_fields = ["name", "number"]
    filterset_fields = ["name", "number", "process__name", "process__key"]
    ordering_fields = ["id", "create_time"]
    ordering = ["-id"]

    def get_serializer_class(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "attr_value":
            return InstanceHasAttrValueSerializers
        elif serializer == "task_list":
            return InstanceHasTaskSerializers
        else:
            return super().get_serializer_class()


class InstanceTaskViewSet(LoginRequiredMixin, ModelViewSet):
    """
        实例任务信息
    """
    queryset = InstanceTask.objects.all()
    serializer_class = InstanceTaskSerializers
    search_fields = ["name", "key"]
    filterset_fields = ["instance__name", "instance__number", "group__name", "group__alias", "assignee", "status"]
    ordering_fields = ["id", "create_time"]
    ordering = ["-id"]

    def get_serializer_class(self):
        serializer = self.request.query_params.get("serializer")
        if serializer == "group_user":
            return InstanceTaskHasGroupUserSerializers
        return super().get_serializer_class()

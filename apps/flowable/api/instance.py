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

    def get_queryset(self):
        status = self.request.query_params.get("status")
        # 全部流程
        if status == "all":
            return super().get_queryset()
        # 流程池-根据人员分组查询流程
        elif status == "pool":
            instance_task_qs = InstanceTask.objects.filter(group__group_user=self.request.user, status="ing")
            qs = Instance.objects.filter(id__in=[instance_task_q.instance.id for instance_task_q in instance_task_qs],
                                         status__in=["init", "ing"])
            return qs
        # 待办流程
        elif status == "undo":
            instance_task_qs = InstanceTask.objects.filter(assignee__contains=[self.request.user.username],
                                                           status="ing")
            qs = Instance.objects.filter(id__in=[instance_task_q.instance.id for instance_task_q in instance_task_qs],
                                         status__in=["init", "ing"])
            return qs
        # 我的工单
        elif status == "applicant":
            return Instance.objects.filter(applicant=self.request.user)
        # 我的处理
        elif status == "handle":
            instance_task_qs = InstanceTask.objects.filter(assignee__contains=[self.request.user.username])
            qs = Instance.objects.filter(id__in=[instance_task_q.instance.id for instance_task_q in instance_task_qs],
                                         status__in=["init", "ing"])
            return qs
        else:
            return Instance.objects.none()


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

from django.urls import path
from rest_framework.routers import DefaultRouter

from flowable.api.flowable import SubmitView, RepealView, ClaimView, DelegateView, HandleView, ResolveView, DiagramView
from flowable.api.instance import InstanceViewSet, InstanceTaskViewSet
from flowable.api.process import ProcessGroupViewSet, ProcessViewSet, ProcessAttrViewSet

app_name = 'flowable'

router = DefaultRouter()
router.register("process-group", ProcessGroupViewSet, "process-group")  # 流程分组
router.register("process", ProcessViewSet, "process")  # 流程定义
router.register("process-attr", ProcessAttrViewSet, "process-attr")  # 流程属性
router.register("instance", InstanceViewSet, "instance")  # 实例信息
router.register("instance-task", InstanceTaskViewSet, "instance-task")  # 实例任务

urlpatterns = [
    path("submit", SubmitView.as_view(), name="submit"),  # 提交工单
    path("repeal", RepealView.as_view(), name="repeal"),  # 撤销工单
    path("claim", ClaimView.as_view(), name="claim"),  # 认领任务
    path("delegate", DelegateView.as_view(), name="delegate"),  # 指派任务
    path("resolve", ResolveView.as_view(), name="resolve"),  # 指派任务
    path("handle", HandleView.as_view(), name="handle"),  # 处理/审批工单
    path("diagram", DiagramView.as_view(), name="diagram"),  # 获取流程图
]

urlpatterns += router.urls

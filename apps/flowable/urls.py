from django.urls import path
from rest_framework.routers import DefaultRouter

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

]

urlpatterns += router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter

from flowable.api.instance import InstanceViewSet, InstanceTaskViewSet
from flowable.api.process import ProcessGroupViewSet, ProcessViewSet, ProcessAttrViewSet

app_name = 'flowable'

router = DefaultRouter()
router.registry("process-group", ProcessGroupViewSet, "process-group")  # 流程分组
router.registry("process", ProcessViewSet, "process")  # 流程定义
router.registry("process-attr", ProcessAttrViewSet, "process-attr")  # 流程属性
router.registry("instance", InstanceViewSet, "instance")  # 实例信息
router.registry("instance-task", InstanceTaskViewSet, "instance-task")  # 实例任务

urlpatterns = [

]

urlpatterns += router.urls

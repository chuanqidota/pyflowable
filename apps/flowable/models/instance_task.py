from django.db import models
from django.utils.translation import gettext_lazy as _

from flowable.models.instance import Instance
from user.models import BaseModel, Group


class InstanceTask(BaseModel):
    STATUS_CHOICE = (
        ('init', _('初始化')),
        ('ing', _('执行中')),
        ('finish', _('完成')),
        ('error', _('错误')),
    )

    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name="instance_task",
                                 db_constraint=False, help_text=_("实例"), db_comment=_("实例"))
    group = models.ManyToManyField(Group, related_name="group_task", db_constraint=False, help_text=_("组"))
    name = models.CharField(max_length=100, help_text=_("中文名称"), db_comment=_("中文名称"))
    key = models.CharField(max_length=100, help_text=_("英文名称"), db_comment=_("英文名称"))
    assignee = models.JSONField(default=list, help_text=_("分配人"), db_comment="分配人")
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, help_text=_("状态"), db_comment=_("状态"))
    params = models.JSONField(default=dict, help_text=_("参数"), db_comment=_("参数"))

    class Meta:
        db_table = "instance_task"
        verbose_name = "实例任务"
        app_label = "flowable"

    @property
    def group_display(self) -> str:
        """
            组名称
        :return:
        """
        return ",".join([i.name for i in self.group.all()])

    @property
    def group_user_list(self):
        """
            组用户
        :return:
        """
        return self.group.group_user.all().values() if self.group else []

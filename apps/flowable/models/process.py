from django.db import models
from django.utils.translation import gettext_lazy as _

from flowable.models.process_group import ProcessGroup
from user.models import BaseModel, User


class Process(BaseModel):
    group = models.ForeignKey(ProcessGroup, on_delete=models.PROTECT, related_name="group_process", db_constraint=False,
                              help_text=_("流程分组"), db_comment=_("流程分组"))
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_mentor", db_constraint=False,
                               help_text=_("流程顾问"), db_comment=_("流程顾问"))
    name = models.CharField(max_length=50, help_text=_("中文名称"), db_comment=_("中文名称"))
    key = models.CharField(max_length=50, unique=True, help_text=_("模型key"), db_comment=_("模型key"))
    sort = models.IntegerField(help_text=_("排序"), db_comment=_("排序"))

    class Meta:
        verbose_name = "流程定义"
        app_label = "flowable"

    @property
    def mentor_display(self):
        """
            流程顾问展示
        :return:
        """
        return f"{self.mentor.name}-{self.mentor.username}"

    @property
    def instance_list(self):
        """
            流程实例列表
        :return:
        """
        return self.process_instance.all()

    @property
    def attr_list(self):
        return self.process_attr.all()

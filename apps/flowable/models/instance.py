import ast

from django.db import models
from django.utils.translation import gettext_lazy as _

from flowable.models.process import Process
from user.models import BaseModel, User


class Instance(BaseModel):
    STATUS_CHOICE = (
        ('init', _('初始化')),
        ('ing', _('执行中')),
        ('cancel', _('取消')),
        ('complete', _('完成')),
    )
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                                related_name="process_instance", help_text=_("流程定义"), db_comment=_("流程定义"))
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                                  related_name="user_applicant", help_text=_("申请人"), db_comment=_("申请人"))
    flowable_id = models.CharField(max_length=50, help_text=_("flowable流程示例ID"), db_comment=_("flowable流程示例ID"))
    name = models.CharField(max_length=100, help_text=_("名称"), db_comment=_("名称"))
    number = models.CharField(max_length=100, help_text=_("编号"), db_comment=_("编号"))
    status = models.CharField(choices=STATUS_CHOICE, default="init", max_length=50, help_text=_("状态"),
                              db_comment=_('状态'))
    record = models.JSONField(default=list, help_text=_("操作记录"), db_comment="操作记录")

    class Meta:
        verbose_name = "流程实例"
        app_label = "flowable"

    @property
    def instance_attr_value_dict(self):
        """
            实例属性值
        :return:
        """
        attr_values = self.instance_attr_value.all()
        result = {}
        for attr_value in attr_values:
            code = attr_value.attr.code
            _type = attr_value.attr.type
            value = attr_value.value
            result[code] = value if _type == "str" else ast.literal_eval(value)
        return result

    @property
    def task_list(self):
        """
            任务列表
        :return:
        """
        return self.instance_task.all().values()

    @property
    def applicant_display(self) -> str:
        """
            申请人展示
        :return:
        """
        return f"{self.applicant.name}-{self.applicant.username}" if self.applicant else ""

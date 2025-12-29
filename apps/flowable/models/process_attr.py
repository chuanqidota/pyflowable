from django.db import models
from django.utils.translation import gettext_lazy as _

from flowable.models.process import Process
from user.models import BaseModel


class ProcessAttr(BaseModel):
    TYPE_CHOICES = (
        ("str", _("字符串")),
        ("int", _("数字")),
        ("list", _("列表")),
        ("dict", _("字典")),
        ("bool", _("布尔")),
    )

    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, blank=True, related_name="process_attr",
                                db_constraint=False, help_text=_("流程定义"), db_comment=_("流程定义"))
    name = models.CharField(max_length=100, help_text=_("属性中文名"), db_comment=_("属性中文名"))
    code = models.CharField(max_length=100, help_text=_("属性英文名"), db_comment=_("属性英文名"))
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, help_text=_("属性类型"), db_comment=_("属性类型"))

    class Meta:
        verbose_name = "流程属性"
        app_label = "flowable"

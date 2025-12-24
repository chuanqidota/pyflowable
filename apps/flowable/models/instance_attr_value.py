from django.db import models
from django.utils.translation import gettext_lazy as _

from flowable.models.instance import Instance
from flowable.models.process_attr import ProcessAttr
from user.models import BaseModel


class InstanceAttrValue(BaseModel):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, related_name="instance_attr_value",
                                 db_constraint=False, help_text=_("实例"), db_comment=_("实例"))
    attr = models.ForeignKey(ProcessAttr, on_delete=models.SET_NULL, related_name="attr_value",
                             db_constraint=False, help_text=_("属性"), db_comment=_("属性"))
    value = models.TextField(help_text=_("属性值"), db_comment=_("属性值"))

    class Meta:
        verbose_name = "实例属性值"
        app_label = "flowable"

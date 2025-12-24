from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import BaseModel


class ProcessGroup(BaseModel):
    name = models.CharField(max_length=50, unique=True, help_text=_("名称"), db_comment=_('名称'))
    sort = models.IntegerField(help_text=_("排序"), db_comment=_("排序"))

    class Meta:
        verbose_name = "流程分组"
        app_label = "flowable"

    @property
    def process_list(self):
        """
            流程列表
        :return:
        """
        return self.group_process.all()

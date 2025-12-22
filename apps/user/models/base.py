from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, help_text=_('创建时间'), db_comment=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, help_text=_('更新时间'), db_comment=_('更新时间'))
    description = models.TextField(null=True, blank=True, help_text=_('说明'), db_comment=_('说明'))
    is_delete = models.BooleanField(default=False, verbose_name=_('逻辑删除'), db_comment=_('逻辑删除'))

    class Meta:
        abstract = True
        verbose_name = '基础模型'
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import BaseModel


class Group(BaseModel):
    name = models.CharField(max_length=50, unique=True, help_text='组名称', db_comment=_('用户组名称'))
    alias = models.CharField(max_length=100, null=True, blank=True, help_text='组别名', db_comment=_('用户组别名'))

    class Meta:
        verbose_name = '用户组'
        app_label = 'user'

    @property
    def user_list(self):
        return self.group_user.filter(is_active=True).values(*["username", "name", "email"])

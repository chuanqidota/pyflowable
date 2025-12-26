from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models.base import BaseModel
from user.models.group import Group
from utils.crypt import signer


class User(BaseModel):
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'username'

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_user", db_constraint=False,
                              null=True, blank=True,
                              help_text='所属组', db_comment=_('所属用户组'))
    username = models.CharField(max_length=150, unique=True, help_text='用户名', db_comment=_('用户名'))
    name = models.CharField(max_length=150, help_text='姓名', db_comment=_('姓名'))
    _password = models.CharField(max_length=100, null=True, blank=True, db_comment=_('密码'))
    email = models.EmailField(unique=True, help_text='电子邮件', db_comment=_('电子邮件'))
    is_active = models.BooleanField(default=True, help_text='是否激活', db_comment=_('是否激活'))

    objects = UserManager()

    class Meta:
        verbose_name = '用户'
        app_label = 'user'

    @property
    def password(self):
        return signer.decrypt(self._password)

    @password.setter
    def password(self, dat):
        self._password = signer.encrypt(dat)

    def check_password(self, password):
        if not self._password:
            return False
        return password == self.password

    @property
    def is_anonymous(self):
        return False

    @property
    def is_staff(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def group_name(self):
        """
            组名称
        :return:
        """
        return f"{self.group.name}-{self.group.alias}" if self.group else ""

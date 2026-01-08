from flowable.utils.flowable import flowable_handle
from user.models import Group


class ActionGroup:

    @staticmethod
    def create_group(name, alias):
        """
            创建用户组
        :param name:
        :param alias:
        :return:
        """
        qs = Group.objects.filter(alias=alias)
        if not qs:
            Group.objects.create(name=name, alias=alias)
        flowable_handle.create_group(alias, name)

    @staticmethod
    def delete_group(alias):
        """
            删除用户组
        :param alias:
        :return:
        """
        Group.objects.filter(alias=alias).delete()
        flowable_handle.delete_group(alias)

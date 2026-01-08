from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from flowable.utils.flowable import flowable_handle
from user.models import Group


@receiver(post_save, sender=Group)
def create_group(sender, instance=None, created=False, **kwargs):
    if created:
        print(instance.alias, instance.name)
        if not flowable_handle.create_group(instance.alias, instance.name):
            raise ValueError("flowable创建组失败")


@receiver(post_delete, sender=Group)
def delete_group(sender, instance=None, **kwargs):
    if not flowable_handle.delete_group(instance.alias):
        raise ValueError("flowable删除组失败")

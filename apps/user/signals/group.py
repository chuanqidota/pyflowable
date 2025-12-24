from django.db.models.signals import post_save
from django.db.models.signals import post_delete

from django.dispatch import receiver

from user.models import Group


@receiver(post_save, sender=Group)
def create_group(sender, instance=None, created=False, **kwargs):
    if created:
        # 执行创建组后的操作
        print(f'Group {instance.name} has been created.')


@receiver(post_delete, sender=Group)
def delete_group(sender, instance=None, **kwargs):
    # 执行删除组后的操作
    print(f'Group {instance.name} has been deleted.')

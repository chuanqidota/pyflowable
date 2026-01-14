from celery import shared_task

from flowable.service.flowable import ActionHandle
from user.models import User


@shared_task
def flowable_task_demo():
    print(1)


@shared_task
def handle_task(user_id, instance_id, allow):
    """
        处理工单
    :param user_id: 用户id
    :param instance_id: 实例id
    :param allow: 1:通过，0:驳回
    :return:
    """
    user = User.objects.filter(id=user_id).first()
    ActionHandle(user).handle(instance_id, allow)

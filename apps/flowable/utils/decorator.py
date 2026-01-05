import json
from functools import wraps

from flowable.models.instance_task import InstanceTask
from flowable.utils.response import FailResp


def kwargs_required(*required_args):
    """
        参数存不存在校验
    :param required_args:
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            for arg in required_args:
                if arg not in json.loads(request.body):
                    return FailResp(msg=f"参数没有传: {arg}")
            return func(*args, **kwargs)

        return wrapper

    return decorate


def update_instance_task(func):
    """
        更新实例任务状态信息
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = kwargs.get("instance")
        key = func.__name__
        instance_qs = InstanceTask.objects.filter(instance=instance, key=key)
        instance_qs.update(status="ing", params=kwargs)
        try:
            r = func(*args, **kwargs)
        except Exception as e:
            instance_qs.update(status="error")
            raise Exception(repr(e))
        else:
            instance_qs.update(status="finish")
        return r

    return wrapper

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
            if request.method == "GET":
                data_source = request.GET
            else:  # POST, PUT, PATCH, DELETE 等
                # 如果是JSON格式
                if request.content_type == 'application/json':
                    try:
                        data_source = json.loads(request.body)
                    except json.JSONDecodeError:
                        return FailResp(msg="无效的json格式")
                else:
                    # 普通表单格式
                    data_source = request.POST
            errors = []
            for arg in required_args:
                value = data_source.get(arg)
                if value is None or (isinstance(value, str) and value.strip() == ''):
                    errors.append(arg)
            if errors:
                return FailResp(msg=f"缺少参数: {errors}")
            return func(request, *args, **kwargs)

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

from functools import wraps

from flowable.models.instance import Instance
from flowable.models.instance_task import InstanceTask
from flowable.utils.flowable import flowable_handle
from utils.response import FailResp


def kwargs_required(*required_args):
    """
        参数存不存在校验
    :param required_args:
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(instance, request, *args, **kwargs):
            if request.method == "GET":
                data_source = request.query_params
            else:
                data_source = request.data
            errors = []
            for arg in required_args:
                value = data_source.get(arg)
                if value is None or (isinstance(value, str) and value.strip() == ''):
                    errors.append(arg)
            if errors:
                return FailResp(msg=f"缺少参数: {errors}")
            return func(instance, request, *args, **kwargs)

        return wrapper

    return decorate


def finish_task(func):
    """
        完成本次任务
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        instance_id = kwargs.get("instance_id")
        task_id = kwargs.get("task_id")
        flowable_id = kwargs.get("flowable_id")

        diagram = flowable_handle.get_diagram(flowable_id)
        task_key = func.__name__
        instance_qs = InstanceTask.objects.filter(instance__id=instance_id, key=task_key)
        instance_qs.update(status="ing", params=kwargs)
        instance = Instance.objects.filter(id=instance_id)
        instance.update(diagram=diagram)
        try:
            r = func(*args, **kwargs)
            if isinstance(r, dict):
                # 完成任务
                username = r.get("username", None)
                variables = r.get("variables", None)
                f_state, msg = flowable_handle.complete_task(task_id, username=username, variables=variables)
                if not f_state:
                    raise ValueError(f"flowable完成任务失败: {msg}")
                instance_qs.update(status="finish")
                diagram = flowable_handle.get_diagram(flowable_id)
                instance.update(diagram=diagram)

                # 下一个任务
                next_task_key = flowable_handle.get_tasks(flowable_id)[0].get("taskDefinitionKey")
                instance_task = InstanceTask.objects.filter(instance__id=instance_id, key=next_task_key).first()
                if instance_task:
                    if username:
                        instance_task.assignee = instance_task.assignee + [username]
                    if variables and variables.get("assigneeList") and isinstance(variables.get("assigneeList"), list):
                        instance_task.assignee = instance_task.assignee + variables.get("assigneeList")
                    instance_task.status = "ing"
                    instance_task.save()
        except Exception as e:
            instance_qs.update(status="error")
            raise ValueError(f"任务执行失败：{repr(e)}")
        return r

    return wrapper


def complete_task(func):
    """
        完成所有任务
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        task_id = kwargs.get("task_id")
        instance_id = kwargs.get("instance_id")
        flowable_id = kwargs.get("flowable_id")
        f_state, msg = flowable_handle.complete_task(task_id)
        if not f_state:
            raise ValueError(f"flowable完成任务失败: {msg}")
        task_key = func.__name__
        InstanceTask.objects.filter(instance__id=instance_id, key=task_key).update(status="finish",
                                                                                   params=kwargs)
        diagram = flowable_handle.get_diagram(flowable_id)
        Instance.objects.filter(id=instance_id).update(status="complete", diagram=diagram)
        flowable_handle.delete_process_instance(flowable_id)
        return r

    return wrapper

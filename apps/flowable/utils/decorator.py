import importlib
import traceback
from functools import wraps
from operator import methodcaller

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
        flowable_id = kwargs.get("flowable_id")
        task_key = func.__name__

        # 执行之前保存流程图
        instances = Instance.objects.filter(id=instance_id)
        instances.update(diagram=flowable_handle.get_diagram(flowable_id))

        # 把将要执行的任务置为执行中
        instance_tasks = InstanceTask.objects.filter(instance__id=instance_id, key=task_key)
        instance_tasks.update(status="ing", params=kwargs)

        try:
            r = func(*args, **kwargs)
            if isinstance(r, dict):
                # 函数的返回值
                variables = r.get("variables", None)  # 下一个任务参数
                assignee = r.get("assignee", None)  # 下一个任务指定分配人
                reject = r.get("reject", {})  # 清理不必要的任务，驳回 以后之前的节点需要清空
                auto_next_task = r.get("auto_next_task", False)  # 自动执行下一个任务

                # 完成本次任务
                tasks = flowable_handle.get_tasks(flowable_id)
                if not tasks:
                    raise ValueError("flowable没有找到任务")
                f_state, msg = flowable_handle.complete_task(tasks[0].get("id"), assignee=assignee, variables=variables)
                if not f_state:
                    raise ValueError(f"flowable完成任务失败: {msg}")
                instances.update(diagram=flowable_handle.get_diagram(flowable_id))
                instance_tasks.update(status="finish")

                # 如果是驳回,则回到目标任务上，同时把其他任务清空
                if reject:
                    # reject = {"target":str,"clean":list,"assigneeList":list,"assignee":str}
                    target = reject.get("target")
                    clean = reject.get("clean", [])
                    assignee_list = reject.get("assigneeList", [])
                    assignee = reject.get("assignee")
                    InstanceTask.objects.filter(instance__id=instance_id, key__in=clean).update(status="init",
                                                                                                assignee=[],
                                                                                                params={})
                    instance_task = InstanceTask.objects.filter(instance__id=instance_id, key=target).first()
                    instance_task.status = "ing"
                    if assignee:
                        instance_task.assignee = list(set(instance_task.assignee + [assignee]))
                    if assignee_list:
                        instance_task.assignee = list(set(instance_task.assignee + assignee_list))
                    instance_task.save()
                    return r

                # 下一个任务
                next_task_key = flowable_handle.get_tasks(flowable_id)[0].get("taskDefinitionKey")
                next_instance_task = InstanceTask.objects.filter(instance__id=instance_id, key=next_task_key).first()
                if next_instance_task:
                    if assignee:
                        next_instance_task.assignee = next_instance_task.assignee + [assignee]
                    if variables and variables.get("assigneeList") and isinstance(variables.get("assigneeList"), list):
                        next_instance_task.assignee = next_instance_task.assignee + variables.get("assigneeList")
                    next_instance_task.status = "ing"
                    next_instance_task.save()

                # 自动执行下一个任务
                if auto_next_task:
                    caller = methodcaller(next_task_key, **kwargs)
                    module = importlib.import_module("apps.flowable.process")
                    model = getattr(module, instances.first().process.key)
                    caller(model())
        except Exception as e:
            instance_tasks.update(status="error")
            raise ValueError(f"任务执行失败：{repr(e)}{traceback.format_exc()}")
        return r

    return wrapper


def complete_task(func):
    """
        最终完成任务
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        instance_id = kwargs.get("instance_id")
        flowable_id = kwargs.get("flowable_id")
        tasks = flowable_handle.get_tasks(flowable_id)
        if not tasks:
            raise ValueError("flowable没有找到任务")
        task_id = tasks[0].get("id")
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

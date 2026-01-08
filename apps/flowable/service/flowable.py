import datetime
import importlib
from operator import methodcaller

from django.conf import settings

from flowable.models.instance import Instance
from flowable.models.instance_attr_value import InstanceAttrValue
from flowable.models.instance_task import InstanceTask
from flowable.models.process import Process
from flowable.models.process_attr import ProcessAttr
from flowable.utils.flowable import flowable_handle
from user.models import User, Group


class ActionHandle:

    def __init__(self):
        self.business_key = settings.FLOWABLE_BUSINESS_KEY

    def submit(self, process_key, username, name, number=None, extra_attrs=None):
        """
            提交工单
        :param process_key: 流程定义的key
        :param username: 申请人英文名
        :param name: 工单名称
        :param number: 工单编号
        :param extra_attrs: dict 表单参数
        :return:
        """
        # 流程
        if not number:
            number = f"NO{datetime.datetime.now().strftime('%Y%m%d%H%M%D')}"
        process = Process.objects.filter(key=process_key).first()
        if not process:
            return False, f"没有流程定义: {process_key}"

        # 申请人
        applicant = User.objects.filter(username=username).first()
        if not applicant:
            return False, f"没有申请人: {username}"

        # 启动流程
        start_state, flowable_id = flowable_handle.start_process(process_key, self.business_key)
        if not start_state:
            return False, f"flowable无法开启流程"

        # 创建流程实例
        instance_data = {
            "process": process,
            "applicant": applicant,
            "flowable_id": flowable_id,
            "name": name,
            "number": number,
            "status": "ing"
        }
        instance = Instance.objects.create(**instance_data)

        # 创建任务
        task_groups = flowable_handle.get_latest_process_task(process_key)
        for item in task_groups:
            name = item.get("name")
            key = item.get("key")
            group = item.get("group", [])
            instance_task = InstanceTask.objects.create(
                instance=instance,
                name=name,
                key=key,
                status="init"
            )
            group_qs = Group.objects.filter(alias__in=group)
            instance_task.group.set(group_qs)

        # 创建实例属性
        process_attr_qs = ProcessAttr.objects.filter(process=process).filter(code__in=list(extra_attrs.keys()))
        attr_value_bulk_data = []
        for process_attr_q in process_attr_qs:
            attr_value_bulk_data.append(InstanceAttrValue(
                instance=instance,
                attr=process_attr_q,
                value=str(extra_attrs.get(process_attr_q.code))
            ))
        InstanceAttrValue.objects.bulk_create(attr_value_bulk_data)

        # 构建参数
        task = flowable_handle.get_tasks(flowable_id)[0]
        task_key = task.get("taskDefinitionKey")
        task_id = task.get("id")
        kwargs = instance.instance_attr_value_dict
        kwargs.update({
            "instance_id": instance.id,
            "process_id": process.id,
            "flowable_id": instance.flowable_id,
            "task_id": task_id
        })
        # 反射对应函数
        caller = methodcaller(task_key, **kwargs)
        module = importlib.import_module("apps.flowable.process")
        model = getattr(module, process_key)
        caller(model())
        return True, "执行成功"

    @staticmethod
    def repeal(instance_id):
        """
            撤销流程
        :param instance_id: 流程实例ID
        :return:
        """
        instance = Instance.objects.filter(id=instance_id).first()
        if not instance:
            return False, f"没于流程示例: {instance_id}"

        flowable_handle.delete_process_instance(instance.flowable_id)
        instance.status = "cancel"
        instance.save()
        return True, "执行成功"

    @staticmethod
    def claim(instance_id, username):
        """
            认领任务
        :param instance_id: 流程实例ID
        :param username: 用户英文名
        :return:
        """
        instance = Instance.objects.filter(id=instance_id).first()
        if not instance:
            return False, f"没有流程示例: {instance_id}"

        tasks = flowable_handle.get_tasks(instance.flowable_id)
        if not tasks:
            return False, f"没有任务: {instance_id}"

        task_id = tasks[0].get("id")
        task_key = tasks[0].get("taskDefinitionKey")

        claim_state, claim_msg = flowable_handle.claim_task(task_id, username)
        if not claim_state:
            return False, f"人员: {username} 认领失败: {claim_msg}"

        InstanceTask.objects.filter(instance=instance, key=task_key).update(**{"assignee": [username]})

        return True, "执行成功"

    @staticmethod
    def delegate(instance_id, username):
        """
            指派任务
        :param instance_id: 流程实例ID
        :param username: 用户英文名
        :return:
        """
        instance = Instance.objects.filter(id=instance_id).first()
        if not instance:
            return False, f"没有流程示例: {instance_id}"

        tasks = flowable_handle.get_tasks(instance.flowable_id)
        if not tasks:
            return False, f"没有任务: {instance_id}"

        task_id = tasks[0].get("id")
        task_key = tasks[0].get("taskDefinitionKey")

        assign_state, assign_msg = flowable_handle.assign_task(task_id, username)
        if not assign_state:
            return False, f"人员: {username} 指派失败: {assign_msg}"

        InstanceTask.objects.filter(instance=instance, key=task_key).update(**{"assignee": [username]})

        return True, "执行成功"

    @staticmethod
    def resolve(instance_id):
        """
            退回任务
        :param instance_id: 流程实例ID
        :return:
        """
        instance = Instance.objects.filter(id=instance_id).first()
        if not instance:
            return False, f"没有流程示例: {instance_id}"
        tasks = flowable_handle.get_tasks(instance.flowable_id)
        if not tasks:
            return False, f"没有任务: {instance_id}"

        task_id = tasks[0].get("id")
        task_key = tasks[0].get("taskDefinitionKey")

        resolve_state, resolve_msg = flowable_handle.resolve_task(task_id)
        if not resolve_state:
            return False, f"退回失败: {resolve_msg}"

        InstanceTask.objects.filter(instance=instance, key=task_key).update(**{"assignee": []})

        return True, "执行成功"

    @staticmethod
    def handle(instance_id, allow, username):
        """
            审批处理工单
        :param instance_id: 流程实例ID
        :param allow: allow是flowable网关上的变量
        :param username: 用户英文名
        :return:
        """
        instance = Instance.objects.filter(id=instance_id).first()
        if not instance:
            raise ValueError("没有查询到实例信息")
        process_key = instance.process.key
        flowable_id = instance.flowable_id
        tasks = flowable_handle.get_tasks(flowable_id)
        if not tasks:
            raise ValueError("flowable没有找到任务")

        task_key = tasks[0].get("taskDefinitionKey")
        task_id = tasks[0].get("id")
        print(task_key, instance.id, username)
        if not InstanceTask.objects.filter(instance=instance, key=task_key, assignee__contains=[username]).exists():
            raise ValueError("人员不在审批节点")

        kwargs = instance.instance_attr_value_dict
        kwargs.update({
            "instance_id": instance.id,
            "process_id": instance.process.id,
            "flowable_id": instance.flowable_id,
            "task_id": task_id,
            "username": username,
            "allow": allow
        })
        # 反射对应函数
        caller = methodcaller(task_key, **kwargs)
        module = importlib.import_module("apps.flowable.process")
        model = getattr(module, process_key)
        caller(model())

    @staticmethod
    def get_diagram(instance_id):
        """
            获取流程图
        :param instance_id: 流程实例ID
        :return:
        """
        diagram = flowable_handle.get_diagram(instance_id)
        return diagram

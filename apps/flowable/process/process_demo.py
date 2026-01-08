from flowable.utils.decorator import finish_task, complete_task


class AppApplyProcess:

    @finish_task
    def submit_task(self, *args, **kwargs):
        print("submit_task kwargs:", kwargs)
        return {"variables": {"assigneeList": ["xiaoa"]}}  # 这里返回的是装饰器的参数,用于下一个任务的参数,这里是审批节点的人员

    @finish_task
    def leader_task(self, *args, **kwargs):
        print("leader_task kwargs:", kwargs)
        return {"variables": {"allow": 1}}  # 里返回的是装饰器的参数,用于下一个任务的参数,网关的参数

    @complete_task
    def sor_task(self, *args, **kwargs):
        print("sor_task kwargs:", kwargs)

from flowable.utils.decorator import finish_task, complete_task
from flowable.utils.next_task import next_approval, next_gateway_agree, next_gateway_reject, next_auto_task


class AppApplyProcess:

    @finish_task
    def submit_task(self, *args, **kwargs):
        print("submit_task kwargs:", kwargs)
        return next_approval(["xiaoa"])  # 下一个审批审批节点

    @finish_task
    def leader_task(self, *args, **kwargs):
        print("leader_task kwargs:", kwargs)
        if kwargs.get("allow") == 1:
            return next_gateway_agree(auto_next_task=True)  # 网关节点且让后面的任务自动执行
        else:
            return next_gateway_reject(target="submit_task", clean=["leader_task"])  # 驳回到那个节点，清楚哪些节点

    @finish_task
    def sor_task(self, *args, **kwargs):
        print("sor_task kwargs:", kwargs)
        return next_auto_task()  # 自动执行下一个节点

    @complete_task
    def dba_task(self, *args, **kwargs):
        print("dba_task kwargs:", kwargs)

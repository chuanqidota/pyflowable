class NextTask:

    @staticmethod
    def next_approval(assignee_list=None, assignee=None):
        """
            下一个节点是审批节点
        :param assignee_list:
        :param assignee:
        :return:
        """
        res = dict()
        if assignee_list:
            res["variables"] = {"assigneeList": assignee_list}
        if assignee:
            res["assignee"] = assignee
        return res

    @staticmethod
    def next_gateway_agree(auto_next_task, assignee_list=None, assignee=None):
        """
            下一个节点是网关节点
        :param auto_next_task: 自动执行下一个任务
        :param assignee_list: 下一个任务如果需要分配参数
        :param assignee: 下一个节点分配人
        :return:
        """
        res = dict()
        res["variables"] = {"allow": 1}
        if auto_next_task:
            res["auto_next_task"] = True
        if assignee_list:
            res["variables"].update({"assigneeList": assignee_list})
        if assignee:
            res["assignee"] = assignee
        return res

    @staticmethod
    def next_gateway_reject(target, clean, assignee=None, assigneeList=None):
        """
            下一个节点是网关节点-驳回
        :param target: 驳回到那个节点
        :param clean: 需要清理哪些已经执行的节点
        :param assignee: 目标节点的人
        :param assigneeList: 目标节点的人列表
        :return:
        """
        res = dict()
        res["variables"] = {"allow": 0}
        res["reject"] = {"target": target, "clean": clean, "assignee": assignee, "assigneeList": assigneeList}
        return res

    @staticmethod
    def next_auto_task():
        return {"auto_next_task": True}


next_approval = NextTask.next_approval
next_gateway_agree = NextTask.next_gateway_agree
next_gateway_reject = NextTask.next_gateway_reject
next_auto_task = NextTask.next_auto_task

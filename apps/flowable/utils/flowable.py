import requests

from django.conf import settings


class FlowableHandler:
    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint
        self.username = username
        self.password = password

        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({'Content-Type': 'application/json'})
        self.url_prefix = f"{self.endpoint}/flowable-rest/service"
        self.url_config = {
            "get_groups": f"{self.url_prefix}/identity/groups",  # 查询用户组列表
            "create_group": f"{self.url_prefix}/identity/groups",  # 创建用户组
            "delete_group": f"{self.url_prefix}/identity/groups/{{group_id}}",  # 删除用户组

            "start_process": f"{self.url_prefix}/runtime/process-instances",  # 启动流程
            "process_definitions": f"{self.url_prefix}/repository/process-definitions",  # 查询流程版本定义
            "process_model": f"{self.url_prefix}/repository/process-definitions/{{process_id}}/model",  # 查询流程详情
            "process_instance": f"{self.url_prefix}/runtime/process-instances/{{process_instance_id}}",  # 获取流程实例信息
            "historic_process_instances": f"{self.url_prefix}/history/historic-process-instances",  # 历史流程实例查询
            "delete_process_instance": f"{self.url_prefix}/runtime/process-instances/{{process_instance_id}}",  # 删除流程实例
            "diagram": f"{self.url_prefix}/repository/process-instances/{{process_instance_id}}/diagram",  # 获取流程图

            "historic_tasks": f"{self.url_prefix}/history/historic-task-instances",  # 历史任务查询
            "task_identity_links": f"{self.url_prefix}/runtime/tasks/{{task_id}}/identitylinks",  # 任务候选人/组
            "tasks": f"{self.url_prefix}/runtime/tasks",  # 获取任务列表
            "complete_task": f"{self.url_prefix}/runtime/tasks/{{task_id}}",  # 完成任务
            "action_task": f"{self.url_prefix}/runtime/tasks/{{task_id}}",  # 认领
        }

    def get_groups(self):
        """
            获取用户组列表
        :return:
            [{"id":"OpsManager","name":"运维管理员组"}]
        """
        url = self.url_config["get_groups"]
        response = self.session.get(url)
        print(response.text)
        res = response.json()
        return [{"id": i.get("id"), "name": i.get("name")} for i in res.get("data")]

    def create_group(self, group_id, name, _type=None):
        """
            创建分组
        :param group_id:
        :param name:
        :param _type:
        :return:
            True/False
        """
        url = self.url_config["create_group"]
        payload = {
            "id": group_id,
            "name": name,
        }
        if _type:
            payload["type"] = _type
        response = self.session.post(url, json=payload)
        print(response.text)
        if response.ok:
            return False
        return True

    def delete_group(self, group_id):
        """
        删除用户组
        
        :param self: 说明
        :param group_id: 说明 组ID
        """
        url = self.url_config["delete_group"].format(group_id=group_id)
        response = self.session.delete(url)
        print(response.text)
        if response.status_code != 204:
            return False
        return True

    def start_process(self, process_definition_key, business_key=None, variables=None):
        """
            启动流程
        :param self: 说明
        :param process_definition_key: 说明 模型key
        :param business_key: 说明 业务key
        :param variables: 说明 流程变量
        :return:
            True/False, 流程示例ID
        """
        url = self.url_config["start_process"]
        payload = {
            "processDefinitionKey": process_definition_key,
        }
        if business_key:
            payload["businessKey"] = business_key
        if variables:
            payload["variables"] = [{"name": k, "value": v} for k, v in variables.items()]
        response = self.session.post(url, json=payload)
        print(response.text)
        if not response.ok:
            return False, None
        return True, response.json().get("id")

    def get_latest_process_task(self, process_definition_key):
        """
            获取最新版本流程中的所有task和分组
        :param process_definition_key:
        :return:
            [{
                'key': 'submit_task',
                'group': ['OpsManager'],
                'name': '提交工单'
            }, {
                'key': 'leader_task',
                'group': ['OpsManager'],
                'name': '领导审批'
            }, {
                'key': 'sor_task',
                'group': ['OpsManager'],
                'name': 'sor处理'
            }]
        """
        process_definitions_url = self.url_config["process_definitions"]
        params = {
            "key": process_definition_key
        }
        process_def_res = self.session.get(process_definitions_url, params=params)
        process_id = process_def_res.json().get("data")[-1].get("id")
        process_model_url = self.url_config["process_model"].format(process_id=process_id)
        process_model_res = self.session.get(process_model_url)
        tasks = process_model_res.json().get("processes")[0].get("flowElementMap")
        return [{"key": t, "group": tasks.get(t).get("candidateGroups"), "name": tasks.get(t).get("name")}
                for t in tasks.keys() if t.endswith("_task")]

    def get_process_instance(self, process_instance_id):
        """
        流程实例信息
        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        :return:
            {
                'id': '7a491c38-e563-11f0-9ec7-0242ac120002',
                'url': 'http://127.0.0.1:8081/flowable-rest/service/runtime/process-instances/7a491c38-e563-11f0-9ec7-0242ac120002',
                'name': None,
                'businessKey': 'pyflowable',
                'businessStatus': None,
                'suspended': False,
                'ended': False,
                'processDefinitionId': 'appApplyProcess:14:462bb2bf-db2f-11f0-8f57-0242ac150003',
                'processDefinitionUrl': 'http://127.0.0.1:8081/flowable-rest/service/repository/process-definitions/appApplyProcess:14:462bb2bf-db2f-11f0-8f57-0242ac150003',
                'processDefinitionName': '应用申请流程',
                'processDefinitionDescription': None,
                'activityId': None,
                'startUserId': 'rest-admin',
                'startTime': '2025-12-30T09:39:46.462Z',
                'variables': [],
                'callbackId': None,
                'callbackType': None,
                'referenceId': None,
                'referenceType': None,
                'propagatedStageInstanceId': None,
                'tenantId': '',
                'completed': False
            }
        """
        url = self.url_config["process_instance"].format(process_instance_id=process_instance_id)
        response = self.session.get(url)
        print(response.text)
        if not response.ok:
            return None
        return response.json()

    def delete_process_instance(self, process_instance_id, reason=None):
        """
            删除流程实例
        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        :param reason: 说明 删除原因
        :return: True/False
        """
        url = self.url_config["delete_process_instance"].format(process_instance_id=process_instance_id)
        params = {}
        if reason:
            params["reason"] = reason
        response = self.session.delete(url, params=params)
        print(response.text)
        if response.status_code != 204:
            return False
        return True

    def get_historic_process_instances(self, business_key=None):
        """
        获取历史流程实例
        
        :param self: 说明
        :param business_key: 说明 业务key
        """
        url = self.url_config["historic_process_instances"]
        params = {}
        if business_key:
            params["businessKey"] = business_key
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_process_diagram(self, process_instance_id):
        """
        获取流程图
        
        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        """
        url = self.url_config["diagram"].format(process_instance_id=process_instance_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def get_tasks(self, process_instance_id=None, assignee=None, candidate_user=None, candidate_group=None):

        """
        获取任务列表
        
        :param self: 说明
        :param assignee: 说明 分配人
        :param candidate_user: 说明 候选用户
        :param candidate_group: 说明 候选组
        :param process_instance_id: 说明 流程实例ID

        响应示例:
        -----------
             {
                "data": [
                    {
                    "id": "89cd5718-dbb3-11f0-9b16-0242ac150002",
                    "url": "http://127.0.0.1:8081/flowable-rest/service/runtime/tasks/89cd5718-dbb3-11f0-9b16-0242ac150002",
                    "owner": null,
                    "assignee": null,
                    "delegationState": null,
                    "name": "提交工单",
                    "description": null,
                    "createTime": "2025-12-18T01:47:40.604Z",
                    "dueDate": null,
                    "priority": 50,
                    "suspended": false,
                    "claimTime": null,
                    "taskDefinitionKey": "submit_task",
                    "scopeDefinitionId": null,
                    "scopeId": null,
                    "subScopeId": null,
                    "scopeType": null,
                    "propagatedStageInstanceId": null,
                    "tenantId": "",
                    "category": null,
                    "formKey": null,
                    "parentTaskId": null,
                    "parentTaskUrl": null,
                    "executionId": "89ccbad4-dbb3-11f0-9b16-0242ac150002",
                    "executionUrl": "http://127.0.0.1:8081/flowable-rest/service/runtime/executions/89ccbad4-dbb3-11f0-9b16-0242ac150002",
                    "processInstanceId": "89cba960-dbb3-11f0-9b16-0242ac150002",
                    "processInstanceUrl": "http://127.0.0.1:8081/flowable-rest/service/runtime/process-instances/89cba960-dbb3-11f0-9b16-0242ac150002",
                    "processDefinitionId": "appApplyProcess:14:462bb2bf-db2f-11f0-8f57-0242ac150003",
                    "processDefinitionUrl": "http://127.0.0.1:8081/flowable-rest/service/repository/process-definitions/appApplyProcess:14:462bb2bf-db2f-11f0-8f57-0242ac150003",
                    "variables": []
                    }
                ],
                "total": 1,
                "start": 0,
                "sort": "id",
                "order": "asc",
                "size": 1
                }
        """
        url = self.url_config["tasks"]
        params = {}
        if assignee:
            params["assignee"] = assignee
        if candidate_user:
            params["candidateUser"] = candidate_user
        if candidate_group:
            params["candidateGroup"] = candidate_group
        if process_instance_id:
            params["processInstanceId"] = process_instance_id
        response = self.session.get(url, params=params)
        if not response.ok:
            return False, response.text
        return response.json().get("data")

    def complete_task(self, task_id, user_id=None, variables=None):
        """
        完成任务
        
        :param self: 说明
        :param task_id: 说明 任务ID
        :param user_id: 说明 用户ID
        :param variables: 说明 流程变量
        """
        url = self.url_config["complete_task"].format(task_id=task_id)
        payload = {
            "action": "complete",
        }
        if user_id:
            payload["assignee"] = user_id
        if variables:
            payload["variables"] = [{"name": k, "value": v} for k, v in variables.items()]
        response = self.session.post(url, json=payload)
        if not response.ok:
            return False, response.text
        return True, response.text

    def claim_task(self, task_id, username):
        """
        认领任务
        
        :param self: 说明
        :param task_id: 说明 任务ID
        :param username: 说明 用户英文名称
        """
        url = self.url_config["action_task"].format(task_id=task_id)
        payload = {
            "action": "claim",
            "assignee": username
        }
        response = self.session.post(url, json=payload)
        if not response.ok:
            return False, response.text
        return True, response.text

    def assign_task(self, task_id, username):
        """
        指派任务

        :param self: 说明
        :param task_id: 说明 任务ID
        :param username: 说明 用户英文名称
        """
        url = self.url_config["action_task"].format(task_id=task_id)
        payload = {
            "action": "delegate",
            "assignee": username
        }
        response = self.session.put(url, json=payload)
        if not response.ok:
            return False, response.text
        return True, response.text

    def resolve_task(self, task_id):
        """
        退回任务

        :param self: 说明
        :param task_id: 说明 任务ID
        """
        url = self.url_config["action_task"].format(task_id=task_id)
        payload = {
            "action": "resolve"
        }
        response = self.session.put(url, json=payload)
        if not response.ok:
            return False, response.text
        return True, response.text

    def get_task_assignee_group(self, task_id):
        """
        获取任务候选人/组
        
        :param self: 说明
        :param task_id: 说明 任务ID
        """
        url = self.url_config["task_identity_links"].format(task_id=task_id)
        response = self.session.get(url)
        if not response.ok:
            return False, response.text
        return True, [i.get("group") for i in response.json() if i.get("group")]

    def get_historic_tasks(self, process_instance_id=None, assignee=None):
        """
        获取历史任务

        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        :param assignee: 说明 分配人
        """
        url = self.url_config["historic_tasks"]
        params = {}
        if process_instance_id:
            params["processInstanceId"] = process_instance_id
        if assignee:
            params["assignee"] = assignee
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()


flowable_handle = FlowableHandler(settings.FLOWABLE_HOST, settings.FLOWABLE_USERNAME, settings.FLOWABLE_PASSWORD)

if __name__ == '__main__':
    _endpoint = "http://127.0.0.1:8081"
    _username = "rest-admin"
    _password = "test"
    handle = FlowableHandler(_endpoint, _username, _password)

    # groups = handle.get_groups()
    # print(groups)

    # res = handle.create_group("sorManager", "sor管理")
    # print(res)

    # res = handle.delete_group("sorManager")
    # print(res)

    res = handle.get_latest_process_task("appApplyProcess")
    print(res)

    # res = handle.start_process("appApplyProcess", "pyflowable")
    # print(res)

    # res = handle.get_process_instance("7a491c38-e563-11f0-9ec7-0242ac120002")
    # print(res)

    # res = handle.delete_process_instance("7a491c38-e563-11f0-9ec7-0242ac120002")
    # print(res)

    # res = handle.get_historic_process_instances()
    # print(res)

    # res = handle.get_tasks("b43d214f-e9db-11f0-a8fb-0242ac140002")
    # print(res)

    # res = handle.complete_task("b450a957-e9db-11f0-a8fb-0242ac140002", variables={"assigneeList": ["admin"]})
    # print(res)

    # res = handle.get_task_assignee_group("0f7fdcd5-e9dc-11f0-a8fb-0242ac140002")
    # print(res)

    # res = handle.complete_task("26dcc026-e91d-11f0-8571-0242ac130002", variables={"pass":"1"})
    # print(res)

    # res = handle.delete_process_instance("4280adfa-dbb8-11f0-8f57-0242ac150003")
    # print(res)
    #
    # res = handle.get_historic_tasks("4280adfa-dbb8-11f0-8f57-0242ac150003")
    # print(res)

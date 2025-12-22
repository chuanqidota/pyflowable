import requests

class FlowableHandler:
    def __init__(self,endpoint,username,password):
        self.endpoint = endpoint
        self.username = username
        self.password = password

        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({'Content-Type': 'application/json'})
        self.url_prefix = f"{self.endpoint}/flowable-rest/service"
        self.url_config = {
            "get_groups": f"{self.url_prefix}/identity/groups", # 查询用户组列表
            "create_group": f"{self.url_prefix}/identity/groups", # 创建用户组
            "delete_group": f"{self.url_prefix}/identity/groups/{{group_id}}", # 删除用户组

            "start_process": f"{self.url_prefix}/runtime/process-instances", # 启动流程
            "process_instance": f"{self.url_prefix}/runtime/process-instances/{{process_instance_id}}", # 获取流程实例信息
            "historic_process_instances": f"{self.url_prefix}/history/historic-process-instances", # 历史流程实例查询
            "delete_process_instance": f"{self.url_prefix}/runtime/process-instances/{{process_instance_id}}", # 删除流程实例
            "diagram": f"{self.url_prefix}/repository/process-instances/{{process_instance_id}}/diagram", # 获取流程图

            "historic_tasks": f"{self.url_prefix}/history/historic-task-instances", # 历史任务查询
            "task_identity_links": f"{self.url_prefix}/runtime/tasks/{{task_id}}/identitylinks", # 任务候选人/组
            "tasks": f"{self.url_prefix}/runtime/tasks", # 获取任务列表
            "complete_task": f"{self.url_prefix}/runtime/tasks/{{task_id}}", # 完成任务
            "claim_task": f"{self.url_prefix}/runtime/tasks/{{task_id}}", # 认领
            "assign_task": f"{self.url_prefix}/runtime/tasks/{{task_id}}" # 指派
            
        }
    
    def get_groups(self):
        """
        获取用户组列表
        """
        url = self.url_config["get_groups"]
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def create_group(self,group_id,name,type=None):
        """
        创建用户组
        
        :param self: 说明
        :param group_id: 说明 组ID
        :param name: 说明 组名称
        :param type: 说明 组类型
        """
        url = self.url_config["create_group"]
        payload = {
            "id": group_id,
            "name": name,
        }
        if type:
            payload["type"] = type
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def delete_group(self,group_id):
        """
        删除用户组
        
        :param self: 说明
        :param group_id: 说明 组ID
        """
        url = self.url_config["delete_group"].format(group_id=group_id)
        response = self.session.delete(url)
        response.raise_for_status()
        return response.status_code == 204
    
    def start_process(self,process_definition_key,business_key=None,variables=None):
        """
        启动流程
        
        :param self: 说明
        :param process_definition_key: 说明 模型key
        :param business_key: 说明 业务key
        :param variables: 说明 流程变量
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
        response.raise_for_status()
        return response.json()

    def get_process_instance(self,process_instance_id):
        """
        流程实例信息

        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        """
        url = self.url_config["process_instance"].format(process_instance_id=process_instance_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def delete_process_instance(self,process_instance_id,reason=None):
        """
        删除流程实例

        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        :param reason: 说明 删除原因
        """
        url = self.url_config["delete_process_instance"].format(process_instance_id=process_instance_id)
        params = {}
        if reason:
            params["reason"] = reason
        response = self.session.delete(url, params=params)
        response.raise_for_status()
        return response.status_code == 204

    def get_historic_process_instances(self,business_key=None):
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

    def get_process_diagram(self,process_instance_id):
        """
        获取流程图
        
        :param self: 说明
        :param process_instance_id: 说明 流程实例ID
        """ 
        url = self.url_config["diagram"].format(process_instance_id=process_instance_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def get_tasks(self,assignee=None,candidate_user=None,candidate_group=None,process_instance_id=None,active=True):
        """
        获取任务列表
        
        :param self: 说明
        :param assignee: 说明 分配人
        :param candidate_user: 说明 候选用户
        :param candidate_group: 说明 候选组
        :param process_instance_id: 说明 流程实例ID
        :param active: 说明 是否仅查询未完成任务

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
        response.raise_for_status()
        return response.json()

    def complete_task(self,task_id,variables=None):
        """
        完成任务
        
        :param self: 说明
        :param task_id: 说明 任务ID
        :param variables: 说明 流程变量
        """
        url = self.url_config["complete_task"].format(task_id=task_id)
        payload = {}
        if variables:
            payload["variables"] = [{"name": k, "value": v} for k, v in variables.items()]
        response = self.session.post(f"{url}/complete", json=payload)
        response.raise_for_status()
        return response.json()
    
    def claim_task(self,task_id,user_id):
        """
        认领任务
        
        :param self: 说明
        :param task_id: 说明 任务ID
        :param user_id: 说明 用户ID
        """
        url = self.url_config["claim_task"].format(task_id=task_id)
        payload = {
            "action": "claim",
            "assignee": user_id
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def assign_task(self,task_id,user_id):
        """
        指派任务

        :param self: 说明
        :param task_id: 说明 任务ID
        :param user_id: 说明 用户ID
        """
        url = self.url_config["assign_task"].format(task_id=task_id)
        payload = {
            "assignee": user_id
        }
        response = self.session.put(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_task_identity_links(self,task_id):
        """
        获取任务候选人/组
        
        :param self: 说明
        :param task_id: 说明 任务ID
        """
        url = self.url_config["task_identity_links"].format(task_id=task_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_historic_tasks(self,process_instance_id=None,assignee=None):
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

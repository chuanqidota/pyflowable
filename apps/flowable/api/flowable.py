from rest_framework.views import APIView

from flowable.service.flowable import ActionHandle
from flowable.utils.decorator import kwargs_required
from flowable.utils.response import SuccessResp, FailResp
from user.mixins.login import LoginRequiredMixin


class SubmitView(LoginRequiredMixin, APIView):
    """
        提交工单
    """

    @kwargs_required("process_key", "name", "number", "extra_attrs")
    def post(self, request):
        data = request.data
        process_key = data.get("process_key")
        name = data.get("name")
        number = data.get("number")
        extra_attrs = data.get("extra_attrs")
        username = request.user.username
        submit_state, submit_msg = ActionHandle().submit(process_key, username, name, number, extra_attrs)
        return SuccessResp(submit_msg) if submit_state else FailResp(submit_msg)


class RepealView(LoginRequiredMixin, APIView):
    """
        撤销工单
    """

    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        repeal_state, repeal_msg = ActionHandle().repeal(instance_id)
        return SuccessResp(repeal_msg) if repeal_state else FailResp(repeal_msg)


class ClaimView(LoginRequiredMixin, APIView):
    """
        认领任务
    """

    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        username = request.user.username
        claim_state, claim_msg = ActionHandle().claim(instance_id, username)
        return SuccessResp(claim_msg) if claim_state else FailResp(claim_msg)


class DelegateView(LoginRequiredMixin, APIView):
    """
        指派任务
    """

    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        username = request.user.username
        delegate_state, delegate_msg = ActionHandle().delegate(instance_id, username)
        return SuccessResp(delegate_msg) if delegate_state else FailResp(delegate_msg)


class ResolveView(LoginRequiredMixin, APIView):
    """
        退回任务
    """

    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        resolve_state, resolve_msg = ActionHandle().resolve(instance_id)
        return SuccessResp(resolve_msg) if resolve_state else FailResp(resolve_msg)


class HandleView(LoginRequiredMixin, APIView):
    """
        审批工单
    """

    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        allow = data.get("allow")
        username = request.user.username
        ActionHandle().handle(instance_id, allow, username)
        return SuccessResp(msg="后台执行中")


class DiagramView(LoginRequiredMixin, APIView):
    """
        获取流程图
    """

    @kwargs_required("instance_id")
    def get(self, request):
        instance_id = request.query_params.get("instance_id")
        diagram = ActionHandle().get_diagram(instance_id)
        return SuccessResp(result={"diagram": diagram})

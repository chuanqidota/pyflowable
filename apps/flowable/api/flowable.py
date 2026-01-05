from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from flowable.service.flowable import FlowableActionHandle
from flowable.utils.response import SuccessResp, FailResp
from user.mixins.login import LoginRequiredMixin


class SubmitView(LoginRequiredMixin, APIView):
    """
        提交工单
    """

    def post(self, request):
        data = request.data
        process_key = data.get("process_key")
        name = data.get("name")
        number = data.get("number")
        extra_attrs = data.get("extra_attrs")
        username = request.user.username
        submit_state, submit_msg = FlowableActionHandle().submit(process_key, username, name, number, extra_attrs)
        return SuccessResp(submit_msg) if submit_state else FailResp(submit_msg)


class RepealView(LoginRequiredMixin, APIView):
    """
        撤销工单
    """

    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        repeal_state, repeal_msg = FlowableActionHandle().repeal(instance_id)
        return SuccessResp(repeal_msg) if repeal_state else FailResp(repeal_msg)


class ClaimView(LoginRequiredMixin, APIView):
    """
        认领任务
    """

    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        username = request.user.username
        claim_state, claim_msg = FlowableActionHandle().claim(instance_id, username)
        return SuccessResp(claim_msg) if claim_state else FailResp(claim_msg)


class DelegateView(LoginRequiredMixin, APIView):
    """
        指派任务
    """

    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        username = request.user.username
        delegate_state, delegate_msg = FlowableActionHandle().delegate(instance_id, username)
        return SuccessResp(delegate_msg) if delegate_state else FailResp(delegate_msg)


class ResolveView(LoginRequiredMixin, APIView):
    """
        退回任务
    """

    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        resolve_state, resolve_msg = FlowableActionHandle().resolve(instance_id)
        return SuccessResp(resolve_msg) if resolve_state else FailResp(resolve_msg)


class HandleView(LoginRequiredMixin, APIView):
    """
        审批工单
    """

    def post(self, request):
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)

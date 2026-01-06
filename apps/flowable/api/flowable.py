from drf_spectacular.utils import inline_serializer, extend_schema, OpenApiExample
from rest_framework import serializers
from rest_framework.views import APIView

from flowable.service.flowable import ActionHandle
from flowable.utils.decorator import kwargs_required
from flowable.utils.response import SuccessResp, FailResp
from user.mixins.login import LoginRequiredMixin


class SubmitView(LoginRequiredMixin, APIView):
    """
        提交工单
    """

    @extend_schema(
        summary='提交工单',
        request=inline_serializer(
            name='SubmitRequestSerializer',
            fields={
                'process_key': serializers.CharField(help_text='流程标识键'),
                'name': serializers.CharField(help_text='工单名称'),
                'number': serializers.CharField(help_text='工单编号'),
                'extra_attrs': serializers.DictField(help_text='额外参数')
            }
        ),
        tags=["工单操作"]
    )
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

    @extend_schema(
        summary='撤销工单',
        request=inline_serializer(
            name='RepealRequestSerializer',
            fields={'instance_id': serializers.IntegerField(help_text='实例ID')}
        ),
        tags=["工单操作"]
    )
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

    @extend_schema(
        summary='认领工单',
        request=inline_serializer(
            name='ClaimRequestSerializer',
            fields={'instance_id': serializers.IntegerField(help_text='实例ID')}
        ),
        tags=["工单操作"]
    )
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

    @extend_schema(
        summary='指派工单',
        request=inline_serializer(
            name='DelegateRequestSerializer',
            fields={'instance_id': serializers.IntegerField(help_text='实例ID')}
        ),
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        username = request.user.username
        delegate_state, delegate_msg = ActionHandle().delegate(instance_id, username)
        return SuccessResp(delegate_msg) if delegate_state else FailResp(delegate_msg)


class ResolveView(LoginRequiredMixin, APIView):
    """
        退回工单
    """

    @extend_schema(
        summary='退回工单',
        request=inline_serializer(
            name='ResolveRequestSerializer',
            fields={'instance_id': serializers.IntegerField(help_text='实例ID')}
        ),
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        resolve_state, resolve_msg = ActionHandle().resolve(instance_id)
        return SuccessResp(resolve_msg) if resolve_state else FailResp(resolve_msg)


class HandleView(LoginRequiredMixin, APIView):
    """
        处理/审批工单
    """

    @extend_schema(
        summary='处理/审批工单',
        request=inline_serializer(
            name='HandleRequestSerializer',
            fields={
                'instance_id': serializers.IntegerField(help_text='实例ID'),
                'allow': serializers.IntegerField(help_text='是否通过')
            }
        ),
        tags=["工单操作"]
    )
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

    @extend_schema(
        summary='获取流程图',
        request=inline_serializer(
            name='DiagramRequestSerializer',
            fields={'instance_id': serializers.IntegerField(help_text='实例ID')}
        ),
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def get(self, request):
        instance_id = request.query_params.get("instance_id")
        diagram = ActionHandle().get_diagram(instance_id)
        return SuccessResp(result={"diagram": diagram})

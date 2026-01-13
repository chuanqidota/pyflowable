from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import serializers
from rest_framework.views import APIView

from flowable.service.flowable import ActionHandle
from flowable.utils.decorator import kwargs_required
from utils.response import SuccessResp, FailResp
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
        responses={
            200: inline_serializer(
                name='SubmitSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("process_key", "name", "extra_attrs")
    def post(self, request):
        data = request.data
        process_key = data.get("process_key")
        name = data.get("name")
        number = data.get("number")
        extra_attrs = data.get("extra_attrs")
        user = request.user
        username = user.username
        try:
            submit_state, submit_msg = ActionHandle(user).submit(process_key, name, number, extra_attrs)
            return SuccessResp(submit_msg) if submit_state else FailResp(submit_msg)
        except Exception as e:
            return FailResp(repr(e))


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
        responses={
            200: inline_serializer(
                name='RepealSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        try:
            repeal_state, repeal_msg = ActionHandle(request.user).repeal(instance_id)
            return SuccessResp(repeal_msg) if repeal_state else FailResp(repeal_msg)
        except Exception as e:
            return FailResp(repr(e))


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
        responses={
            200: inline_serializer(
                name='ClaimSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        try:
            claim_state, claim_msg = ActionHandle(request.user).claim(instance_id)
            return SuccessResp(claim_msg) if claim_state else FailResp(claim_msg)
        except Exception as e:
            return FailResp(repr(e))


class DelegateView(LoginRequiredMixin, APIView):
    """
        指派任务
    """

    @extend_schema(
        summary='指派工单',
        request=inline_serializer(
            name='DelegateRequestSerializer',
            fields={'instance_id': serializers.IntegerField(help_text='实例ID'),
                    'username': serializers.CharField(help_text='用户名')}
        ),
        responses={
            200: inline_serializer(
                name='DelegateSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        username = data.get("username")
        try:
            delegate_state, delegate_msg = ActionHandle(request.user).delegate(instance_id, username)
            return SuccessResp(delegate_msg) if delegate_state else FailResp(delegate_msg)
        except Exception as e:
            return FailResp(repr(e))


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
        responses={
            200: inline_serializer(
                name='ResolveSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        try:
            resolve_state, resolve_msg = ActionHandle(request.user).resolve(instance_id)
            return SuccessResp(resolve_msg) if resolve_state else FailResp(resolve_msg)
        except Exception as e:
            return FailResp(repr(e))


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
        responses={
            200: inline_serializer(
                name='HandleSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def post(self, request):
        data = request.data
        instance_id = data.get("instance_id")
        allow = data.get("allow")
        try:
            ActionHandle(request.user).handle(instance_id, allow)
            return SuccessResp(msg="后台执行中")
        except Exception as e:
            return FailResp(repr(e))


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
        responses={
            200: inline_serializer(
                name='DiagramSuccessResponse',
                fields={
                    'result': serializers.DictField(default={"diagram": ""}),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["工单操作"]
    )
    @kwargs_required("instance_id")
    def get(self, request):
        instance_id = request.query_params.get("instance_id")
        diagram = ActionHandle().get_diagram(instance_id)
        return SuccessResp(result={"diagram": diagram})

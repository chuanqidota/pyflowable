from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.mixins.login import LoginRequiredMixin


class SubmitView(LoginRequiredMixin, APIView):
    """
        提交工单
    """

    def post(self, request):
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)


class RepealView(LoginRequiredMixin, APIView):
    """
        撤销工单
    """

    def post(self, request):
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)


class ClaimView(LoginRequiredMixin, APIView):
    """
        认领任务
    """

    def post(self, request):
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)


class DelegateView(LoginRequiredMixin, APIView):
    """
        指派任务
    """

    def post(self, request):
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)


class HandleView(LoginRequiredMixin, APIView):
    """
        审批工单
    """

    def post(self, request):
        data = request.data
        return Response(data=data, status=status.HTTP_200_OK)

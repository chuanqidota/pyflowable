from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ManualLoginView(APIView):
    permission_classes = (AllowAny,)
    tags = ["登录"]
    operation_id = "手动登录"

    @extend_schema(
        summary='用户登陆',
        request=inline_serializer(
            name='ManualRequestSerializer',
            fields={
                'username': serializers.CharField(help_text='用户名'),
                'password': serializers.CharField(help_text='密码')
            }
        ),
        responses={
            200: inline_serializer(
                name='ManualSuccessResponse',
                fields={
                    'result': serializers.DictField(default=dict),
                    'msg': serializers.CharField(default='执行成功'),
                    'code': serializers.CharField(default="0000")
                }
            )
        },
        tags=["用户"]
    )
    def post(self, request):
        """
            手动登录
        :param request:
        :return:
        """
        username = self.request.data.get('username', '')
        password = self.request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(data={'message': '无效的用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            login(request, user)
            return Response(data={"msg": "登录成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"msg": f"登录失败-{repr(e)}"}, status=status.HTTP_400_BAD_REQUEST)

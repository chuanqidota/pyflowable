from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ManualLoginView(APIView):
    permission_classes = (AllowAny,)
    tags = ["登录"]
    operation_id = "手动登录"

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

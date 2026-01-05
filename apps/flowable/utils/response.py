from rest_framework.response import Response
from rest_framework import status


class SuccessResp(Response):
    """
        成功响应
    """

    def __init__(self, result):
        data = {
            "result": result,
            "code": "0000"
        }
        _status = status.HTTP_200_OK
        super().__init__(data=data, status=_status)


class FailResp(Response):
    """
        失败响应
    """

    def __init__(self, result):
        data = {
            "result": result,
            "code": "0001"
        }
        _status = status.HTTP_200_OK
        super().__init__(data=data, status=_status)

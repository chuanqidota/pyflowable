from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, str):
            data = {'result': None, 'code': "0001", 'msg': exc.detail}
        elif isinstance(exc.detail, list):
            data = {'result': None, 'code': "0001", 'msg': ";".join(exc.detail)}
        elif isinstance(exc.detail, dict):
            data = {'result': None, 'code': "0001", 'msg': ";".join([f"{k}:{v}" for k, v in exc.detail.items()])}
        else:
            data = {'result': None, 'code': "0001", 'msg': exc.detail}
        set_rollback()
        return Response(data, status=status.HTTP_200_OK, headers=headers)

    return None

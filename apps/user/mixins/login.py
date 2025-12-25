from django.contrib.auth.mixins import AccessMixin

from pyflowable import settings


class LoginRequiredMixin(AccessMixin):
    """
        debug模式下不用登录
    """

    def dispatch(self, request, *args, **kwargs):
        # 生产环境强制开启登录验证
        if not settings.DEBUG and not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "user"

    def ready(self):
        from .signals import group
        from .signals import user
        super(UserConfig, self).ready()

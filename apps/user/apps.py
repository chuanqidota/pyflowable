from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "user"
    def ready(self):
        from user.signals import group
        from user.signals import user
        super(UserConfig, self).ready()
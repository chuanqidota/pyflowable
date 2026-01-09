from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        基础序列化
    """
    group_name = serializers.ReadOnlyField(help_text="用户分组")

    class Meta:
        model = User
        fields = list(set([f.name for f in User._meta.get_fields()
                           if not (hasattr(f, 'is_relation') and f.is_relation)])
                      - {"_password"}) + ["group_name", "group"]


class CreateUserSerializer(serializers.ModelSerializer):
    """
        创建序列化
    """
    password = serializers.CharField(help_text="密码")

    class Meta:
        model = User
        fields = list(set([f.name for f in User._meta.get_fields()
                           if not (hasattr(f, 'is_relation') and f.is_relation)])
                      - {"_password"}) + ["password", "group"]

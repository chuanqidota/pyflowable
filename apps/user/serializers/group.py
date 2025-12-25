from rest_framework import serializers

from user.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """
        基础序列化
    """
    class Meta:
        model = Group
        fields = "__all__"


class GroupHasSerializer(serializers.ModelSerializer):
    """
        包含用户的序列化
    """
    user_list = serializers.ReadOnlyField(help_text="用户列表")

    class Meta:
        model = Group
        fields = [f.name for f in Group._meta.get_fields()] + ["user_list"]

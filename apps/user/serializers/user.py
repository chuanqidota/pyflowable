from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(help_text="用户分组")

    class Meta:
        model = User
        fields = list(set([f.name for f in User._meta.get_fields()]) - {"_password"}) + ["group_name"]

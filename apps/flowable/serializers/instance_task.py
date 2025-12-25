from rest_framework import serializers

from flowable.models.instance_task import InstanceTask


class InstanceTaskSerializers(serializers.ModelSerializer):
    """
        基础序列化
    """
    status_display = serializers.SerializerMethodField(help_text="状态")
    group_user_list = serializers.ReadOnlyField(help_text="组用户")
    group_display = serializers.ReadOnlyField(help_text="组名称")

    class Meta:
        model = InstanceTask
        fields = [f.name for f in InstanceTask._meta.get_fields()] + \
                 ["status_display", "group_user_list", "group_display"]

    @staticmethod
    def get_status_display(obj):
        return obj.get_status_display()

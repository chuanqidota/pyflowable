from rest_framework import serializers

from flowable.models.instance import Instance


class InstanceSerializers(serializers.ModelSerializer):
    """
        基础序列化
    """
    status_display = serializers.SerializerMethodField(help_text="状态展示")

    class Meta:
        model = Instance
        fields = [f.name for f in Instance._meta.get_fields()
                  if not (hasattr(f, 'is_relation') and f.is_relation)] + \
                 ["status_display"]

    @staticmethod
    def get_status_display(obj):
        """
            状态展示
        :param obj:
        :return:
        """
        return obj.get_status_display()


class InstanceHasAttrValueSerializers(serializers.ModelSerializer):
    """
        包含实例属性值信息
    """
    status_display = serializers.SerializerMethodField(help_text="状态展示")
    instance_attr_value_dict = serializers.SerializerMethodField(help_text="实例属性值")

    class Meta:
        model = Instance
        fields = [f.name for f in Instance._meta.get_fields()
                  if not (hasattr(f, 'is_relation') and f.is_relation)] + \
                 ["status_display", "instance_attr_value_dict"]

    @staticmethod
    def get_status_display(obj):
        """
            状态展示
        :param obj:
        :return:
        """
        return obj.get_status_display()


class InstanceHasTaskSerializers(serializers.ModelSerializer):
    """
        包含任务列表
    """
    task_list = serializers.ReadOnlyField(help_text="任务列表")

    class Meta:
        model = Instance
        fileds = [f.name for f in Instance._meta.get_fields()
                  if not (hasattr(f, 'is_relation') and f.is_relation)] + \
                 ["task_list"]

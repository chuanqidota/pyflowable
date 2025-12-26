from rest_framework import serializers

from flowable.models.process import Process


class ProcessSerializers(serializers.ModelSerializer):
    """
        基础序列化
    """
    mentor_display = serializers.ReadOnlyField(help_text="流程顾问")

    class Meta:
        model = Process
        fields = [f.name for f in Process._meta.get_fields()] + ["mentor_display"]


class ProcessHasInstanceSerializers(serializers.ModelSerializer):
    """
        带有流程示例的序列化
    """
    instance_list = serializers.ReadOnlyField(help_text="实例列表")

    class Meta:
        model = Process
        fields = [f.name for f in Process._meta.get_fields()] + ["instance_list"]


class ProcessHasAttrSerializers(serializers.ModelSerializer):
    """
        带有属性列表的序列化
    """
    attr_list = serializers.ReadOnlyField(help_text="属性列表")

    class Meta:
        model = Process
        fields = [f.name for f in Process._meta.get_fields()] + ["attr_list"]

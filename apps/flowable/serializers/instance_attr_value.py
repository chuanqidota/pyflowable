from rest_framework import serializers

from flowable.models.instance_attr_value import InstanceAttrValue


class InstanceAttrValueSerializers(serializers.ModelSerializer):
    """
        基础序列化
    """

    class Meta:
        model = InstanceAttrValue
        fields = "__all__"

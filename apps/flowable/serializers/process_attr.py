from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from flowable.models.process_attr import ProcessAttr


class ProcessAttrSerializers(serializers.ModelSerializer):
    """
        基础序列化
    """
    type_display = serializers.SerializerMethodField(help_text="类型中文")

    class Meta:
        model = ProcessAttr
        fields = [f.name for f in ProcessAttr._meta.get_fields()
                  if not (hasattr(f, 'is_relation') and f.is_relation)] + \
                 ["type_display", "process"]

        validators = [
            UniqueTogetherValidator(
                queryset=ProcessAttr.objects.all(),
                fields=['process', 'code']
            )
        ]

    @staticmethod
    def get_type_display(obj) -> str:
        return obj.get_type_display()

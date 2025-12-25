from rest_framework import serializers

from flowable.models.process_attr import ProcessAttr


class ProcessAttrSerializers(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField(help_text="类型中文")

    class Meta:
        model = ProcessAttr
        fields = [f.name for f in ProcessAttr._meta.get_fields()] + ["type_display"]

    @staticmethod
    def get_type_display(obj):
        return obj.get_type_display()

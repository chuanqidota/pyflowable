from rest_framework import serializers

from flowable.models.process_group import ProcessGroup


class ProcessGroupSerializers(serializers.ModelSerializer):
    process_list = serializers.ReadOnlyField(help_text="流程列表")

    class Meta:
        model = ProcessGroup
        fields = [f.name for f in ProcessGroup._meta.get_fields()] + ["process_list"]

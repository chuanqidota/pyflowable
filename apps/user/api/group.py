import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.mixins.login import LoginRequiredMixin
from user.models import Group
from user.serializers.group import GroupSerializer, GroupHasSerializer


class GroupViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    search_fields = ["name", "alias"]
    ordering = ['-id']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GroupHasSerializer
        else:
            return super().get_serializer_class()

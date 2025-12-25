from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.mixins.login import LoginRequiredMixin
from user.models import User
from user.serializers.user import UserSerializer


class UserViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    search_fields = ["group__name", "username", "name", "email"]
    filterset_fields = ['is_active']
    ordering_fields = ["id", "created_at"]
    ordering = ['-id']

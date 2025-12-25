from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'flowable'

router = DefaultRouter()

urlpatterns = [
    path('v1/manual-login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls

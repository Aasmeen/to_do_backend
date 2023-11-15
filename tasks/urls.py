from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BaseAPIView, TaskAPIView

router = DefaultRouter()
router.register(r'task', TaskAPIView, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('base/', BaseAPIView.as_view(), name="base-api")
]

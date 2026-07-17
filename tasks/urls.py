from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, TaskViewSet, LabelViewSet

router = DefaultRouter()

router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'labels', LabelViewSet, basename='label')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
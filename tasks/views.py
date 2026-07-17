from django.shortcuts import render
from rest_framework import viewsets
from .models import workspace, Task, Label
from .serializers import WorkspaceSerializer, TaskSerializer, LabelSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class=WorkspaceSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return workspace.objects.filter(owner=self.request.user).select_related('owner')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class LabelViewSet(viewsets.ModelViewSet):
    serializer_class=LabelSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(workspace__owner=self.request.user).select_related('workspace')
    

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class=TaskSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(workspace__owner=self.request.user).select_related('workspace','assignee').prefetch_related('collaborators','Labels')

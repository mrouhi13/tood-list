from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.tasks.api.v1.serializers import TaskSerializer
from apps.tasks.models import Task
from core.permissions import IsProjectMember


class TaskViewSet(viewsets.ModelViewSet):
    """
    List of all tasks filtered by the authenticated user and project.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return self.queryset.filter(project=self.request.project)

    @method_decorator(transaction.atomic)
    def perform_create(self, serializer):
        serializer.save(project=self.request.project)

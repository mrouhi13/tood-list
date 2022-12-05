from apps.tasks.api.v1.serializers import TaskSerializer
from apps.tasks.models import Task

from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    @method_decorator(transaction.atomic)
    def perform_create(self, serializer):
        serializer.save(project=self.request.project)

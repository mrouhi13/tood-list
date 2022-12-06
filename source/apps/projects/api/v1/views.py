from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api.v1.serializers import (
    MemberSerializer, ProjectSerializer
)
from apps.projects.constants import MemberRole
from apps.projects.models import Member, Project
from core.permissions import IsProjectManager


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Project update and other related actions.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'trace']

    def get_serializer_class(self):
        if self.action == 'add_member':
            return MemberSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return self.queryset.filter(members__in=[self.request.user])

    def perform_create(self, serializer):
        user = self.request.user

        project = serializer.save()
        Member.objects.create(
            user=user,
            project=project,
            role=MemberRole.MANAGER,
        )

    @action(detail=True, methods=['post'], url_path='add-member',
            permission_classes=[IsAuthenticated, IsProjectManager])
    def add_member(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

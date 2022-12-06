from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.projects.constants import MemberRole
from apps.projects.models import Member
from apps.tasks.models import Task
from core.serializers import ProjectFilteredPrimaryKeyRelatedField

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    assignees = ProjectFilteredPrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        many=True,
    )

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['project']

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        member = user.members.get(project=request.project)

        if member.role == MemberRole.DEVELOPER:
            attrs['assignees'] = [member]

        return attrs

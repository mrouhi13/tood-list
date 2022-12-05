from rest_framework.serializers import PrimaryKeyRelatedField


class ProjectFilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context['request']
        project = request.project
        return project.members_set.filter(pk__in=super().get_queryset())

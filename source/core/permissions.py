from rest_framework import permissions

from apps.projects.constants import MemberRole


class IsProjectMember(permissions.BasePermission):
    """
     Allows access only to project members.
    """

    def has_permission(self, request, view):
        return request.project.members_set.filter(user=request.user).exists()


class IsProjectManager(permissions.BasePermission):
    """
     Allows access only to project managers.
    """

    def has_object_permission(self, request, view, obj):
        return obj.members_set.filter(user=request.user,
                                      role=MemberRole.MANAGER).exists()

from rest_framework.permissions import BasePermission

from user.models import USER_ROLES


class TeacherOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == USER_ROLES.get('Teacher')


class StudentOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == USER_ROLES.get('Student')

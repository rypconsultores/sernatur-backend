from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission

__all__ = [
    "IsAuthenticated", "IsSuperuserOrTracerUser",
    "BasePermission"
]


class IsSuperuserOrTracerUser(permissions.BasePermission):
    """
    Allows access only to super users or tracers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and (
                request.user.is_superuser or (
                    hasattr(request.user, 'user_extra_conf')
                    and request.user.user_extra_conf.traceability
                )
            )
        )

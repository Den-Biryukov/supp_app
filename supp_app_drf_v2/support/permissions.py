from rest_framework.permissions import BasePermission


class IsUser(BasePermission):

    def has_permission(self, request, view):

        def is_user_support(user):
            if hasattr(user, 'supports'):
                if request.user.supports.is_support == True:
                    return 1
                else:
                    return 0
            else:
                return 0

        return bool(
            request.user.is_authenticated and not request.user.is_staff
            and not is_user_support(request.user)
        )


class IsAdminOrSupport(BasePermission):

    def has_permission(self, request, view):

        def is_user_support(user):

            if hasattr(user, 'supports'):
                if request.user.supports.is_support == True:
                    return 1
                else:
                    return 0
            else:
                return 0
        return bool(
            request.user.is_staff or is_user_support(request.user)
        )

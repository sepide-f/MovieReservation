from functools import wraps
from django.http import HttpResponseForbidden
from users.models import Role


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            # Ensure the user is authenticated
            if hasattr(view, 'request'):
                # CBV: request is part of the view instance
                request = view.request

            if not request.user.is_authenticated:
                return HttpResponseForbidden("Access Denied: Please log in.")

            try:
                # Get the user's role
                user_role = Role.objects.get(user=request.user).name

                # Check if the user's role matches the required role
                if user_role == required_role:
                    return view_func(view, request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("Access Denied: You do not have the required role.")
            except Role.DoesNotExist:
                # Handle case where user has no role assigned
                return HttpResponseForbidden("Access Denied: No role assigned.")

        return _wrapped_view

    return decorator

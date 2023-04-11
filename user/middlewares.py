"""Middlewares for mycinema app"""

from django.utils import timezone
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token


class AdminAutoLogoutMiddleware:
    """Middleware to automatically log out non-superuser authenticated users
    after a period of inactivity.

    The middleware checks the user's last activity time stored in the session
    and logs them out if the idle time exceeds a certain threshold (30 minutes
    in this case). Additionally, it deletes the user's authentication token,
    if any, to ensure that they cannot use the API after being logged out.

    Attributes:
        get_response: A callable that takes a request and returns a response."""

    def __init__(self, get_response):
        """Initializes a new instance of the `AdminAutoLogoutMiddleware` class."""

        self.get_response = get_response

    def __call__(self, request):
        """Handles an incoming request and returns a response."""

        response = self.get_response(request)

        user = request.user
        if user.is_authenticated and not user.is_superuser:
            last_activity = request.session.get('last_activity')

            if last_activity is not None:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                idle_time = timezone.now() - last_activity
                if idle_time > timezone.timedelta(minutes=30):
                    try:
                        token = Token.objects.get(user=user)
                        token.delete()
                    except Token.DoesNotExist:
                        pass
                    logout(request)

            request.session['last_activity'] = timezone.now().isoformat()

        return response

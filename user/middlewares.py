from django.conf import settings
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.urls import reverse_lazy, reverse


class AdminAutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = request.user
        if user.is_authenticated and not user.is_superuser:
            last_activity = request.session.get('last_activity')

            if last_activity is not None:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                idle_time = timezone.now() - last_activity
                if idle_time > timezone.timedelta(minutes=1):
                    try:
                        token = Token.objects.get(user=user)
                        token.delete()
                    except Token.DoesNotExist:
                        pass
                    logout(request)

            request.session['last_activity'] = timezone.now().isoformat()

        return response



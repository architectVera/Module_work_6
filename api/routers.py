from rest_framework.routers import SimpleRouter
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import LoginView, LogoutView, RegisterView, UsersViewSet
app_name = 'api'

router = SimpleRouter()
router.register(r'users', UsersViewSet, basename="users")

urlpatterns = [
    path('auth/', views.obtain_auth_token, name='api-auth'),
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('', include(router.urls)),
]

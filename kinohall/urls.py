""" URLS for the kinohall app  """

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from kinohall.views import CreateMovieView, MovieDetailView, UpdateMovieView, DeleteMovieView, \
    MovieListView, CreateHallView, HallDetailView, UpdateHallView, \
    DeleteHallView, HallListView, CreateSessionView, SessionDetailView, UpdateSessionView,\
    DeleteSessionView, SessionListView, SessionTodayListView, SessionTomorrowListView


urlpatterns = [
    path('today/', SessionTodayListView.as_view(), name='mycinema'),
    path('tomorrow/', SessionTomorrowListView.as_view(), name='tomorrow-session'),

    path('movie/', MovieListView.as_view(), name='movie-list'),
    path('movie/create/', CreateMovieView.as_view(), name='create-movie'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<int:pk>/update/', UpdateMovieView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', DeleteMovieView.as_view(), name='movie-delete'),

    path('hall/', HallListView.as_view(), name='hall-list'),
    path('hall/create/', CreateHallView.as_view(), name='create-hall'),
    path('hall/<int:pk>/', HallDetailView.as_view(), name='hall-detail'),
    path('hall/<int:pk>/update/', UpdateHallView.as_view(), name='hall-update'),
    path('hall/<int:pk>/delete/', DeleteHallView.as_view(), name='hall-delete'),

    path('session/', SessionListView.as_view(), name='session-list'),
    path('session/create/', CreateSessionView.as_view(), name='create-session'),
    path('session/<int:pk>/', SessionDetailView.as_view(), name='session-detail'),
    path('session/<int:pk>/update/', UpdateSessionView.as_view(), name='session-update'),
    path('session/<int:pk>/delete/', DeleteSessionView.as_view(), name='session-delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

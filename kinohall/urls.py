""" URLS for the kinohall app  """

from django.urls import path
from kinohall.views import film_view, CreateMovieView, MovieDetailView, UpdateMovieView, DeleteMovieView, \
    MovieListView, CreateHallView, HallDetailView, UpdateHallView, \
    DeleteHallView, HallListView, CreateSessionView, SessionDetailView, UpdateSessionView, DeleteSessionView, \
    SessionListView

urlpatterns = [
    path('', film_view, name='mycinema'),

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

]

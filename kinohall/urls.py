""" URLS for the kinohall app  """

from django.urls import path
from kinohall.views import film_view, CreateMovieView, MovieDetailView, UpdateMovieView, DeleteMovieView, MovieListView

urlpatterns = [
    path('', film_view, name='mycinema'),
    path('movie/', MovieListView.as_view(), name='movie-list'),
    path('movie/create/', CreateMovieView.as_view(), name='create-movie'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<int:pk>/update/', UpdateMovieView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', DeleteMovieView.as_view(), name='movie-delete'),
]

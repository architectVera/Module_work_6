from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from kinohall.forms import CreateMovieForm
from kinohall.models import Movie


def film_view(request: HttpRequest):

    return render(request, 'film_list.html')


# All about Movie
class MovieListView(ListView):
    """ This view describes product list """

    model = Movie
    template_name = 'movie_list.html'
    allow_empty = False

    # def get_queryset(self):
    #     """ This method return queryset where attribute available = True """
    #
    #     return Product.objects.filter(available=True)


class MovieDetailView(DetailView):
    """ This view describes details of product """

    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'

    def get_context_data(self, object_list=None, **kwargs):
        """ This method returns a filtered queryset by user """

        context = super().get_context_data(**kwargs)
        return context


class CreateMovieView(UserPassesTestMixin, CreateView):
    """ This view describes create of product """

    model = Movie
    form_class = CreateMovieForm
    template_name = 'movie_create.html'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def form_valid(self, form):
        """Validation"""

        messages.success(self.request, 'Movie created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        """ Method uses action if validation fails"""

        messages.error(self.request, 'Failed to create a movie. Please check the form.')
        return super().form_invalid(form)


class UpdateMovieView(UserPassesTestMixin, UpdateView):
    """ This view describes update of the movie """

    model = Movie
    form_class = CreateMovieForm
    template_name = 'movie_create.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def form_valid(self, form):
        """Validation"""

        messages.success(self.request, 'The Movie update successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        """ Method uses action if validation fails"""

        messages.error(self.request, 'Failed to update the movie. Please check the form.')
        return super().form_invalid(form)


class DeleteMovieView(UserPassesTestMixin, DeleteView):

    model = Movie
    success_url = reverse_lazy('mycinema')
    pk_url_kwarg = 'pk'
    template_name = 'movie_confirm_delete.html'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Movie deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



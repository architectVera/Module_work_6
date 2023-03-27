from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from kinohall.forms import CreateMovieForm, CreateHallForm, CreateSessionForm
from kinohall.models import Movie, Hall, Session


def film_view(request: HttpRequest):

    return render(request, 'film_list.html')


"""MOVIE"""


class MovieListView(ListView):
    """ This view describes product list """

    model = Movie
    template_name = 'movie_list.html'
    allow_empty = False


class MovieDetailView(DetailView):
    """ This view describes details of movie """

    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'

    def get_context_data(self, object_list=None, **kwargs):
        """ This method returns a filtered queryset by user """

        context = super().get_context_data(**kwargs)
        return context


class CreateMovieView(UserPassesTestMixin, CreateView):
    """ This view describes create of movie """

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
    success_url = reverse_lazy('movie-list')
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


"""HALL"""


class HallListView(ListView):
    """ This view describes hall list """

    model = Hall
    template_name = 'hall_list.html'
    allow_empty = False


class HallDetailView(DetailView):
    """ This view describes details of hall """

    model = Hall
    template_name = 'hall_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'

    def get_context_data(self, object_list=None, **kwargs):
        """ This method returns a filtered queryset by user """

        context = super().get_context_data(**kwargs)
        return context


class CreateHallView(UserPassesTestMixin, CreateView):
    """ This view describes create of hall """

    model = Hall
    form_class = CreateHallForm
    template_name = 'hall_create.html'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def form_valid(self, form):
        """Validation"""

        name = form.cleaned_data['name']
        if Hall.objects.filter(name=name).exists():
            messages.error(self.request, 'This name already exists')
            return self.form_invalid(form)

        messages.success(self.request, 'Hall created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        """ Method uses action if validation fails"""

        messages.error(self.request, 'Failed to create a movie. Please check the form.')
        return super().form_invalid(form)


class UpdateHallView(UserPassesTestMixin, UpdateView):
    """ This view describes update of the hall """

    model = Hall
    form_class = CreateHallForm
    template_name = 'hall_create.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def form_valid(self, form):
        """Validation"""

        messages.success(self.request, 'The Hall update successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        """ Method uses action if validation fails"""

        messages.error(self.request, 'Failed to update the hall. Please check the form.')
        return super().form_invalid(form)


class DeleteHallView(UserPassesTestMixin, DeleteView):

    model = Hall
    success_url = reverse_lazy('hall-list')
    pk_url_kwarg = 'pk'
    template_name = 'hall_confirm_delete.html'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Hall deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""SESSION"""
"""SESSION VIEW"""


class SessionListView(ListView):
    """ This view describes product list """

    model = Session
    template_name = 'session_list.html'
    allow_empty = False


class SessionDetailView(DetailView):
    """ This view describes details of movie """

    model = Session
    template_name = 'session_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'

    def get_context_data(self, object_list=None, **kwargs):
        """ This method returns a filtered queryset by user """

        context = super().get_context_data(**kwargs)
        return context


class CreateSessionView(UserPassesTestMixin, CreateView):
    """ This view describes create of session """

    model = Session
    form_class = CreateSessionForm
    template_name = 'session_create.html'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def form_valid(self, form):
        """Validation"""

        messages.success(self.request, 'Hall created successfully')
        return super().form_valid(form)


class UpdateSessionView(UserPassesTestMixin, UpdateView):
    """ This view describes update of the session """

    model = Session
    form_class = CreateSessionForm
    template_name = 'session_create.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def form_valid(self, form):
        """Validation"""

        messages.success(self.request, 'The Session update successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        """ Method uses action if validation fails"""

        messages.error(self.request, 'Failed to update the session. Please check the form.')
        return super().form_invalid(form)


class DeleteSessionView(UserPassesTestMixin, DeleteView):

    model = Session
    success_url = reverse_lazy('session-list')
    pk_url_kwarg = 'pk'
    template_name = 'session_confirm_delete.html'

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Session deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




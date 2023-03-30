from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils.translation import gettext_lazy as _

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from kinohall.forms import CreateMovieForm, CreateHallForm, CreateSessionForm
from kinohall.models import Movie, Hall, Session


# def film_view(request: HttpRequest):
#
#     return render(request, 'today_list.html')
from order.models import Purchase

"""MOVIE"""


class MovieListView(ListView):
    """ This view describes product list """

    model = Movie
    template_name = 'movie_list.html'
    allow_empty = True


class MovieDetailView(DetailView):
    """ This view describes details of movie """

    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'
    allow_empty = True


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
        movie_id = self.kwargs['pk']
        session_with_movie = Session.objects.filter(movie__id__exact=movie_id)
        return self.request.user.is_staff and not session_with_movie.exists()

    def handle_no_permission(self):
        messages.error(self.request, 'You cannot delete movie because it is used in some sessions')
        return redirect('movie-detail', pk=self.kwargs['pk'])

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
    allow_empty = True


class HallDetailView(DetailView):
    """ This view describes details of hall """

    model = Hall
    template_name = 'hall_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'
    allow_empty = True

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

        messages.error(self.request, 'Failed to create a hall. Please check the form.')
        return super().form_invalid(form)


class UpdateHallView(UserPassesTestMixin, UpdateView):
    """ This view describes update of the hall """

    model = Hall
    form_class = CreateHallForm
    template_name = 'hall_create.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """This method checking if user is_staff"""

        hall_id = self.kwargs['pk']
        purchases_with_hall = Purchase.objects.filter(session__hall__id=hall_id, paid=True)
        return self.request.user.is_staff and not purchases_with_hall.exists()

    def handle_no_permission(self):
        messages.error(self.request, 'You cannot update this hall because some tickets have been sold')
        return redirect('hall-detail', pk=self.kwargs['pk'])

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

        hall_id = self.kwargs['pk']
        purchases_with_hall = Purchase.objects.filter(session__hall__id=hall_id, paid=True)
        return self.request.user.is_staff and not purchases_with_hall.exists()

    def handle_no_permission(self):
        messages.error(self.request, 'You cannot delete this hall because some tickets have been sold')
        return redirect('hall-detail', pk=self.kwargs['pk'])

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
    allow_empty = True
    paginate_by = None


class SessionDetailView(DetailView):
    """ This view describes details of movie """

    model = Session
    template_name = 'session_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'
    allow_empty = True


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

        messages.success(self.request, 'Session created successfully')
        return super().form_valid(form)


class UpdateSessionView(UserPassesTestMixin, UpdateView):
    """ This view describes update of the session """

    model = Session
    form_class = CreateSessionForm
    template_name = 'session_create.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """This method checking if user is_staff and there is no purchase with session_id=pk and paid=True"""

        session_id = self.kwargs['pk']
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)
        return self.request.user.is_staff and not purchases_with_session.exists()

    def handle_no_permission(self):
        messages.error(self.request, 'You cannot update this session because some tickets have been sold')
        return redirect('session-detail', pk=self.kwargs['pk'])

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
        """This method checking if user is_staff and there is no purchase with session_id=pk and paid=True"""
        session_id = self.kwargs['pk']
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)
        return self.request.user.is_staff and not purchases_with_session.exists()

    def handle_no_permission(self):
        messages.error(self.request, 'You cannot delete this session because some tickets have been sold')
        return redirect('session-detail', pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Session deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SessionTodayListView(ListView):
    """ This view describes session list """

    model = Session
    template_name = 'today_list.html'
    allow_empty = True

    def get_queryset(self):
        today = timezone.now().date()
        queryset = super().get_queryset()
        return queryset.filter(start_date__lte=today, end_date__gte=today)


class SessionTomorrowListView(ListView):
    """ This view describes session list """

    model = Session
    template_name = 'tomorrow_list.html'
    allow_empty = True

    def get_queryset(self):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        queryset = super().get_queryset()
        return queryset.filter(start_date__lte=tomorrow, end_date__gte=tomorrow)

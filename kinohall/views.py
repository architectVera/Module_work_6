""" Views for the kinohall app  """

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from order.models import Purchase

from kinohall.forms import CreateMovieForm, CreateHallForm, CreateSessionForm
from kinohall.models import Movie, Hall, Session


class MovieListView(UserPassesTestMixin, ListView):
    """ This view describes product list """

    model = Movie
    template_name = 'movie_list.html'
    allow_empty = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class MovieDetailView(DetailView):
    """ This view describes details of movie """

    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'
    allow_empty = True

    def test_func(self):
        """This method checks if user is_staff"""

        return self.request.user.is_staff

    def handle_no_permission(self):
        """Method called when the user does not have permission"""

        messages.error(self.request, 'You do not have permission to access this page')
        return redirect('user-login')

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
    """ This view describes delete of the movie """

    model = Movie
    success_url = reverse_lazy('movie-list')
    pk_url_kwarg = 'pk'
    template_name = 'movie_confirm_delete.html'

    def test_func(self):
        """The test_func method is used to determine whether the user is
          allowed to access the view. It checks if the user is a staff user
          and that there are no sessions associated with the movie being deleted."""

        movie_id = self.kwargs['pk']
        session_with_movie = Session.objects.filter(movie__id__exact=movie_id)
        return self.request.user.is_staff and not session_with_movie.exists()

    def handle_no_permission(self):
        """Method called when the user does not have permission to delete a movie"""

        messages.error(self.request, 'You cannot delete movie because it is used in some sessions')
        return redirect('movie-detail', pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Movie deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the view"""

        context = super().get_context_data(**kwargs)
        return context


class HallListView(UserPassesTestMixin, ListView):
    """ This view describes hall list """

    model = Hall
    template_name = 'hall_list.html'
    allow_empty = True

    def test_func(self):
        """This method checking if user is_staff"""

        return self.request.user.is_staff


class HallDetailView(UserPassesTestMixin, DetailView):
    """ This view describes details of hall """

    model = Hall
    template_name = 'hall_detail.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'
    allow_empty = True


    def test_func(self):
        """ This method checks if the user is staff """

        return self.request.user.is_staff

    def handle_no_permission(self):
        """ Method called when the user does not have permission """

        messages.error(self.request, 'You do not have permission to view this page')
        return redirect('user-login')

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
        """Handle case where user doesn't have permission to update hall"""

        messages.error(self.request, 'You cannot update this hall because some'
                                     ' tickets have been sold')
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
    """View for deleting a Hall object"""

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
        """Handles the case where the user is not authorized to delete the Hall object"""

        messages.error(self.request, 'You cannot delete this hall because some'
                                     ' tickets have been sold')
        return redirect('hall-detail', pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Hall deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Adds extra context data to the view"""

        context = super().get_context_data(**kwargs)
        return context


class SessionListView(ListView):
    """A view that displays a list of movie sessions sorted by start time and price.

        The list can be sorted by price (ascending or descending) or by start time
        (ascending).
        The view uses a queryset of Session model objects.

        Attributes:
            model: A Session model object.
            template_name: A string representing the name of a template.
            allow_empty: A boolean attribute that allows or disallows empty querysets.
            paginate_by: An integer attribute that represents the number of objects per
            page in pagination.

        Methods:
            get_queryset: A method that returns a queryset of Session objects sorted by
            a chosen parameter."""

    model = Session
    template_name = 'session_list.html'
    allow_empty = True
    paginate_by = None

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort')

        if sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == '-price':
            queryset = queryset.order_by('-price')
        elif sort == 'time':
            queryset = queryset.order_by('start_time')
        else:
            queryset = queryset.order_by('start_time', 'price')
        return queryset


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
        """This method checking if user is_staff and there is no purchase
            with session_id=pk and paid=True"""

        session_id = self.kwargs['pk']
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)
        return self.request.user.is_staff and not purchases_with_session.exists()

    def handle_no_permission(self):
        """Action to take if the user does not have permission to update
        the session."""

        messages.error(self.request, 'You cannot update this session because some tickets'
                                     ' have been sold')
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
    """View for deleting a session object. Inherits from UserPassesTestMixin
     and DeleteView."""

    model = Session
    success_url = reverse_lazy('session-list')
    pk_url_kwarg = 'pk'
    template_name = 'session_confirm_delete.html'

    def test_func(self):
        """This method checking if user is_staff and there is no purchase with
         session_id=pk and paid=True"""

        session_id = self.kwargs['pk']
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)
        return self.request.user.is_staff and not purchases_with_session.exists()

    def handle_no_permission(self):
        """Action to take if the user does not have permission to delete
        the session."""

        messages.error(self.request, 'You cannot delete this session because some '
                                     'tickets have been sold')
        return redirect('session-detail', pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        """ Method uses action if object delete"""

        messages.success(self.request, 'Session deleted successfully')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""

        context = super().get_context_data(**kwargs)
        return context


class SessionTodayListView(ListView):
    """ This view describes session list """

    model = Session
    template_name = 'today_list.html'
    allow_empty = True

    def get_queryset(self):
        """ Returns the queryset of sessions taking place on the current day and sorted
        according to the 'sort' query parameter, if provided."""

        today = timezone.now().date()
        queryset = super().get_queryset()
        queryset = queryset.filter(start_date__lte=today, end_date__gte=today)
        sort = self.request.GET.get('sort')

        if sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == '-price':
            queryset = queryset.order_by('-price')
        elif sort == 'time':
            queryset = queryset.order_by('start_time')
        else:
            queryset = queryset.order_by('start_time', 'price')
        return queryset


class SessionTomorrowListView(ListView):
    """ This view describes session list """

    model = Session
    template_name = 'tomorrow_list.html'
    allow_empty = True

    def get_queryset(self):
        """ Returns the queryset of sessions taking place on the next day and sorted
        according to the 'sort' query parameter, if provided."""

        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        queryset = super().get_queryset()
        queryset = queryset.filter(start_date__lte=tomorrow, end_date__gte=tomorrow)
        sort = self.request.GET.get('sort')

        if sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == '-price':
            queryset = queryset.order_by('-price')
        elif sort == 'time':
            queryset = queryset.order_by('start_time')
        else:
            queryset = queryset.order_by('start_time', 'price')
        return queryset

""" Views for the order app  """

from django.contrib import messages

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Session, Purchase, FreeSeatsByDay


def purchase_session(request, pk):
    """
    View function for purchasing tickets for a specific movie session.

    Args:
    request (HttpRequest): The HTTP request object.
    pk (int): The primary key of the session to purchase tickets for.

    Returns:
    HttpResponse: The HTTP response object.

    Raises:
    Http404: If the session with the specified primary key does not exist.

    The function first retrieves the session object from the database using its primary key. It then checks the capacity of the hall where the session is being held, the remaining capacity of the hall after tickets that have already been sold are subtracted, and the free seats available for each day of the session.

    If the request method is POST, the function checks if the selected show date is valid and if the user has sufficient funds to purchase the specified quantity of tickets. It also checks if there are enough tickets available for purchase and creates a new Purchase object if all conditions are met.

    If the request method is not POST, the function simply renders the purchase_session.html template with the session and related information.

    Messages are displayed to the user to indicate any errors that occur during the ticket purchase process.
    """

    session = get_object_or_404(Session, pk=pk)
    hall_capacity = session.hall.seats
    remaining_capacity = 0
    free_seats_by_day = FreeSeatsByDay(session).get_free_seats_by_day()

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        showdata = timezone.datetime.strptime(request.POST.get('showdata'), '%Y-%m-%d').date()
        tickets_sold = Purchase.objects.filter(showdata=showdata, session=session).aggregate(Sum('quantity'))[
                           'quantity__sum'] or 0
        remaining_capacity = hall_capacity - tickets_sold
        current_time = timezone.localtime(timezone.now()).time()

        if showdata < timezone.now().date():
            messages.error(request, 'Show date cannot be less than today')
            return render(request, 'purchase_session.html',
                          {'session': session, 'remaining_capacity': remaining_capacity})

        if showdata == timezone.now().date() and current_time > session.start_time:
            messages.error(request, 'The session has already started. Please choose another session or day')
            return render(request, 'purchase_session.html',
                          {'session': session, 'remaining_capacity': remaining_capacity})

        if showdata > session.end_date:
            messages.error(request, 'You can only select the dates within which films are shown')
            return render(request, 'purchase_session.html',
                          {'session': session, 'remaining_capacity': remaining_capacity})

        if request.user.wallet < session.price * quantity:
            messages.error(request, "You don't have enough money in your account to buy. Please, check your balance")
            return render(request, 'purchase_session.html',
                          {'session': session, 'remaining_capacity': remaining_capacity})

        if remaining_capacity < quantity:
            messages.error(request, f"Only {remaining_capacity} tickets available for purchase")
            return render(request, 'purchase_session.html',
                          {'session': session, 'remaining_capacity': remaining_capacity})

        if quantity <= remaining_capacity:
            purchase = Purchase.objects.create(user=request.user, session=session, quantity=quantity, showdata=showdata)
            request.user.wallet -= session.price * quantity
            request.user.save()
            return redirect('purchase_detail', purchase_id=purchase.id, user_id=request.user.id)

    else:
        return render(request, 'purchase_session.html', {'session': session, 'remaining_capacity': remaining_capacity,
                                                         'free_seats_by_day': free_seats_by_day.items()})


class PurchaseSessionDetailView(DetailView):
    """ This view describes purchase product """

    model = Purchase
    template_name = 'purchase_detail.html'
    pk_url_kwarg = 'purchase_id'
    context_object_name = 'object'
    allow_empty = True

    def get_context_data(self, **kwargs):
        """ This method adds additional context to the view"""

        context = super().get_context_data(**kwargs)
        purchase = context['object']
        total = purchase.get_sum()
        purchase.total = total
        return context


class PurchaseSessionListView(ListView):
    """ This view describes purchase product list """

    model = Session
    template_name = 'purchase_list.html'
    context_object_name = 'object_list'
    allow_empty = True

    def get_queryset(self):
        """ This method return filter queryset by user """

        user = self.request.user
        return Purchase.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        """ This method adds total and return_time to the context """

        context = super().get_context_data(**kwargs)
        total_amount = 0
        for purchase in context['object_list']:
            total = purchase.get_sum()
            purchase.total = total
            total_amount += total
        context['total_amount'] = total_amount
        return context

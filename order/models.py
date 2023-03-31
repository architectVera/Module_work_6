""" Models for the order app  """

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from collections import defaultdict

from django.urls import reverse

from kinohall.models import Session
from user.models import UserModel

User = get_user_model()


class Purchase(models.Model):
    """This class describes the purchase model """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField(default=1)
    showdata = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=True)

    def __str__(self):
        """A string representation of an object"""

        return f"{self.user.username} -Session id: {self.session.id} - {self.session.movie} - Quantity: {self.quantity}"

    def get_sum(self):
        """ The method calculates the total purchase amount"""

        self.total = self.session.price * self.quantity
        return self.total

    def get_absolute_url(self):
        """ This method return absolute url"""

        return reverse('purchase_detail', kwargs={'purchase_id': self.id, 'user_id': self.user.id})


class SoldTicketsByDay:
    def __init__(self, session):
        self.session = session

    def get_sold_tickets_by_day(self):
        sold_tickets_by_day = defaultdict(int)

        purchases = Purchase.objects.filter(session=self.session)

        for purchase in purchases:
            sold_tickets_by_day[purchase.showdata] += purchase.quantity

        return dict(sold_tickets_by_day)

class FreeSeatsByDay:
    def __init__(self, session):
        self.session = session

    def get_free_seats_by_day(self):
        free_seats_by_day = defaultdict(int)

        purchases = Purchase.objects.filter(session=self.session)
        total_seats = self.session.hall.seats

        for purchase in purchases:
            free_seats_by_day[purchase.showdata] += total_seats - purchase.quantity

        return dict(free_seats_by_day)


""" URLS for the product app  """

from django.urls import path
from kinohall.views import film_view

urlpatterns = [
    path('', film_view, name='mycinema'),
]

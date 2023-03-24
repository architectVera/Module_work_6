from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def film_view(request: HttpRequest):

    return render(request, 'film_list.html')

""" Views for the user app  """

from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.urls import reverse_lazy

from django.views import View

from django.contrib.auth import login, logout
from django.contrib import messages

from user.forms import SignUpForm, SignInForm


class UserRegisterView(View):
    """This class describes register view"""

    def get(self, request):
        """ Describes the behaviour when call GET"""

        form = SignUpForm()
        return render(request, 'user_register.html', {'form': form})

    def post(self, request):
        """ Describes the behaviour when call POST"""

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            redirect_url = reverse_lazy('user_login')
            return HttpResponseRedirect(redirect_url)
        messages.error(request, 'Registration failed. Please check the form.')
        return render(request, 'user_register.html', {'form': form})


class UserLoginView(View):
    """Users sing in view

        This view is used to log in whose users who already have an account

        """

    def get(self, request):
        """ Describes the behaviour when call GET"""

        form = SignInForm()
        return render(request, 'user_login.html', {'form': form})

    def post(self, request):
        """ Describes the behaviour when call POST"""

        form = SignInForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            redirect_url = reverse_lazy("myshop")
            return HttpResponseRedirect(redirect_url)
        return render(request, 'user_login.html', {'form': form})


class UserLogoutView(View):
    """This class describes logout view"""

    def get(self, request):
        """ Describes the behaviour when call GET"""

        logout(request)
        redirect_url = reverse_lazy('myshop')
        return HttpResponseRedirect(redirect_url)
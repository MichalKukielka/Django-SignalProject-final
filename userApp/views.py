from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CaptchaUserCreationForm


def index(request):
    return render(request, 'index.html')


@login_required(login_url="/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="/")
def help(request):
    return render(request, 'help.html')

def signup(request):

    if request.method == 'POST':

        form = CaptchaUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/home')


    else:
        form = CaptchaUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views import generic
from django.http import HttpResponse
from .forms import InputSignalForm
from .models import InputSignal
import json


@login_required(login_url="/")
def storage_input(request):

    insta = InputSignal(author=request.user)

    form = InputSignalForm(request.POST, request.FILES, instance=insta)

    if request.method == 'POST':
        if form.is_valid():

            signal = form.save(commit=False)

            signal.save()

            return redirect('storage-main')
    else:
        form = InputSignalForm(instance=insta)

    return render(request,  'storage_input.html', {'form': form})


@login_required(login_url="/")
def storage_list(request):

    signals = InputSignal.objects.filter(author=request.user)

    if request.method == 'DELETE':

        id = str(json.loads(request.body)['id'])
        signal = get_object_or_404(InputSignal, id=id)
        signal.delete()

        return HttpResponse('')

    else:

        return render(request, 'storage_list.html', {'signals': signals})


@login_required(login_url="/")
def storage_main(request):
    return render(request, 'storage_main.html')

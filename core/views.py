from django.shortcuts import redirect, render
from .forms import ClientForm, EnrollmentForm
from .models import Client
from django.shortcuts import render, get_object_or_404

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'core/add_client.html', {'form': form})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def enroll_client(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = EnrollmentForm()
    return render(request, 'core/enroll_client.html', {'form': form})

def client_profile(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'client_profile.html', {'client': client})
from django.shortcuts import render, get_object_or_404
from .models import Client

def client_list(request):
    query = request.GET.get('q')
    clients = Client.objects.filter(full_name__icontains=query) if query else Client.objects.all()
    return render(request, 'core/client_list.html', {'clients': clients})

def client_profile(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'core/client_profile.html', {'client': client})

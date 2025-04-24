from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

from django.test import TestCase
from .models import Client

class ClientModelTest(TestCase):
    def test_create_client(self):
        client = Client.objects.create(full_name="John Doe", age=28, contact="0700000000")
        self.assertEqual(client.full_name, "John Doe")

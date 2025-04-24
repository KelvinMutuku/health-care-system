from django.contrib import admin
from .models import Client, Program, Enrollment

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'age', 'contact']
    search_fields = ['full_name']

admin.site.register(Program)
admin.site.register(Enrollment)

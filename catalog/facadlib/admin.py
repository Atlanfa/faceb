from django.contrib import admin

# Register your models here.
from .models import Advertisement, PagesToMonitor

admin.site.register(Advertisement)
admin.site.register(PagesToMonitor)

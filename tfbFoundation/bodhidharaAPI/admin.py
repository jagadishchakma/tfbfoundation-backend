from django.contrib import admin
from .models import BodhidharaNews

# Register your models here.
@admin.register(BodhidharaNews)
class BodhidharaNewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']
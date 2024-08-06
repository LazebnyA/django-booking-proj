from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'provider_name', 'price', 'author', 'published', 'status')
    list_filter = ('published', 'status')
    search_fields = ('service_name', 'provider_name', 'description')
    prepopulated_fields = {'slug': ('service_name', 'provider_name')}
    date_hierarchy = 'published'
    ordering = ('published', 'price')
    show_facets = admin.ShowFacets.ALWAYS


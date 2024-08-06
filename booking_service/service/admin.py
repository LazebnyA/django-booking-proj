from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'provider_name', 'price', 'author', 'published', 'status')
    list_filter = ('published', 'price', 'status')
    search_fields = ('service_name', 'provider_name', 'description')
    prepopulated_fields = {'slug': ('service_name', 'provider_name')}
    ordering = ('published', 'price')

    # service_name = models.CharField(max_length=100)
    # provider_name = models.CharField(max_length=100)
    # slug = models.SlugField(max_length=100)
    # price = models.IntegerField()
    # description = models.TextField()
    # published = models.DateTimeField(default=timezone.now)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    #
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='services',
    # )
    #
    # status = models.CharField(
    #     choices=Status.choices,
    #     default=Status.DRAFT,
    #     max_length=2
    # )

from django.urls import path

from .views import index

app_name = 'service'

urlpatterns = [
    path('', index, name='index'),
]

from django.urls import path

from service import views

app_name = 'service'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:service_slug>/', views.service_detail, name='service_detail'),
    path('<int:service_id>/share/', views.service_share, name='service_share'),
    path('create/', views.service_create, name='service_create'),
    path('<int:service_id>/comment/', views.service_comment, name='service_comment'),
]

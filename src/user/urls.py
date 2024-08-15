from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.user_dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

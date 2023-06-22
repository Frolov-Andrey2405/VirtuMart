from django.urls import path
from users.views import (
    LoginView, RegistrationView, ProfileView,
    CustomLogoutView, EmailVerificationView)

app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path(
        'verify/<str:email>/<uuid:code>/',
        EmailVerificationView.as_view(), name='email_verification'),
]

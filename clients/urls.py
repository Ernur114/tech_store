from django.urls import path
from .views import RegisterView, register_page, login_page

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-page/', register_page, name='register-page'),
    path('login-page/', login_page, name='login-page'),
]

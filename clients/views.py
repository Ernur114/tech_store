from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import ClientRegisterSerializer, ClientSerializer

Client = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer
    permission_classes = [permissions.AllowAny]


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            Client.objects.create_user(username=username, email=email, password=password1)
            return redirect('/login/')
        else:
            return render(request, 'clients/register.html', {'error': 'Пароли не совпадают!'})

    return render(request, 'clients/register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/swagger/')
        else:
            return render(request, 'clients/login.html', {'error': 'Неверные данные для входа'})
    return render(request, 'clients/login.html')

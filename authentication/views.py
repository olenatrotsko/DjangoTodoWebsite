from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from validate_email import validate_email

from authentication.models import User

def register_user(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password must be at least 6 characters long')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please provide a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR, 'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username is already taken')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email is already taken')
            context['has_error'] = True
        
        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account created successfully')

        return redirect('login')
    
    return render(request, 'authentication/register.html')

def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')
            return render(request, 'authentication/login.html', context)
        
        login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Welcome {username}!')
        return redirect(reverse('home'))
        
    return render(request, 'authentication/login.html')

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')

    return redirect('login')
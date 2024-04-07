from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from validate_email import validate_email

from authentication.models import User
from helpers.decorators import auth_user_should_not_access
from .utils import generate_token

def send_email_verification(user, request):
    current_site = get_current_site(request)    
    subject = 'Please verify your email address'
    email_body = render_to_string('authentication/verify_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    email.send()


@auth_user_should_not_access
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
            return render(request, 'authentication/register.html', context, status=409)


        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email is already taken')
            context['has_error'] = True
            return render(request, 'authentication/register.html', context, status=409)
        
        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()


        send_email_verification(user, request)
        messages.add_message(request, messages.SUCCESS, 'Account created successfully')

        return redirect('login')
    
    return render(request, 'authentication/register.html')

@auth_user_should_not_access
def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Please verify your email address')
            return render(request, 'authentication/login.html', context, status=401)
        
        if not user:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')
            return render(request, 'authentication/login.html', context, status=401)
        
        login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Welcome {username}!')
        return redirect(reverse('home'))
        
    return render(request, 'authentication/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')

    return redirect('login')


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))
    
    return render(request, 'authentication/email_verification_failed.html', status=401)
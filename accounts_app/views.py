from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core_app.models import User
from listing_app.models import Listing
from django.core.mail import send_mail
from django.contrib import messages
import random
import string


def randomString(stringlength=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringlength))


code = randomString()


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        user = User

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password,
        }

        if password == password2:
            if user.objects.filter(username=username).exists():
                messages.error(request, 'Username is already exist!')
                return redirect('register')
            else:
                if user.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already exist!')
                    return redirect('register')
                else:
                    if user.objects.filter(phone=phone).exists():
                        messages.error(request, 'Phone Number is already exist!')
                        return redirect('register')
                    else:
                        send_mail(
                            'Account Registration Confirmation(5 Cent Store)',
                            'Hi ' + first_name + ', Your Confirmation Code is: ' + code,
                            '5centstore.noreply@gmail.com',
                            [email],
                            fail_silently=False
                        )
                        messages.info(request,
                                      ': A confirmation code has been sent to your registered email address, check and confirm your registration')

                        request.method = 'GET'
                        return render(request, 'accounts_app/confirmregister.html', context)
        else:
            messages.error(request, 'Password do not match!')
            return redirect('register')

    else:
        return render(request, 'accounts_app/register.html')


def confirmregister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmcode = request.POST['confirmcode']
        user = User
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'phone': phone,
            'password': password,
        }
        if code == confirmcode:
            user = user.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            login(request, user)
            messages.success(request, 'Registration Confirmed!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Confirmation Code!')
            return render(request, 'accounts_app/confirmregister.html')
    else:
        return redirect('register')


def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ': You are logged in successfully!')
            return redirect('index')
        else:
            messages.error(request, ' Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'accounts_app/login.html')


@login_required
def userlogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


@login_required
def dashboard(request):
    mylistings = Listing.objects.order_by('-list_date').filter(owner=request.user)
    context = {
        'listings': mylistings
    }
    return render(request, 'accounts_app/dashboard.html', context)

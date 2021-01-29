from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('main_home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was Created for ' + user)
                return redirect('login')
        return render(request, 'users/register.html', {'form': form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('main_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(redirect, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    return redirect('main_home')

def send_email(email):
    import smtplib, ssl
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "donateanybook.in@gmail.com"  # Sender address
    receiver_email = email # Enter receiver address
    password = "xxxxxxxx"          #cannot upload password
    subject = "Coupon Code"
    text = """\

    This is to inform you that your book donations has been recieved .

    We thank you for this wonderful gesture and reward you with a small gift from our side .



    Coupon Code : xxxxx

    Restraunt : xxxxxxxxxxxx





    Use this coupon code at any xxxxxxxx outlet and get amazing discounts and benefits *.

    We hope to hear from you again !



    Thanking You

    Regards

    DonateAnyBook



    """

    message =  'Subject: {}\n\n{}'.format(subject, text)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

@login_required(login_url='login')
def profile(request):
    current_user = request.user
    orders = current_user.order_set.all()
    email = current_user.email
    orders_count = current_user.order_set.all().count()
    total_books_recived = current_user.order_set.filter(status='True').count()
    criterion1 = Q(status="True")
    criterion2 = Q(coupon="False")
    total_books_coupon = current_user.order_set.filter(criterion1 & criterion2).count()
    if(total_books_coupon>=5):
        current_user.order_set.filter(criterion1 & criterion2).update(coupon="True")
        send_email(email)
        
    
    context = {
        'orders': orders,
        'username': current_user,
        'email': email,
        'orders_count': orders_count,
        'total_books_recived': total_books_recived,
    }
    return render(request, 'users/profile.html', context)

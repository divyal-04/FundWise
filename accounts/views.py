from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, StudentData
from django.contrib.auth import authenticate, login, logout
from .helpers import send_forget_password_mail
from decimal import Decimal
from django.utils import timezone
from parent.models import ParentProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from uuid import uuid4

# Login view
def Login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.success(request, 'Both Username and Password are required.')
                return redirect('/login/')

            user = authenticate(username=username, password=password)

            if user is None:
                messages.success(request, 'Invalid username or password.')
                return redirect('/login/')

            login(request, user)
            return redirect('/welcome/')  # Redirect to the welcome.html page

    except Exception as e:
        print(e)

    return render(request, 'login.html')

# Register view
def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('/register/')

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is taken.')
                return redirect('/register/')

            if User.objects.filter(email=email).first():
                messages.error(request, 'Email is taken.')
                return redirect('/register/')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            profile_obj = Profile.objects.create(user=user_obj)
            profile_obj.save()
            return redirect('submit_form')  # Redirect to the submit_form view

        except Exception as e:
            print(e)

    return render(request, 'register.html')

# Logout view
def Logout(request):
    logout(request)
    return redirect('/')

# Home view (Login required)
@login_required(login_url='/login/')
def Home(request):
    return render(request, 'home.html')

# ChangePassword view
def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'Password did not match!')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)

# ForgetPassword view
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/forget-password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')

# Submit Form view
def submit_form(request):
    # ... (existing code)
    pass

# Welcome view
def welcome(request):
    if request.user.is_authenticated:
        student_data = request.user.studentdata

        # Retrieve the transaction history with times
        transaction_history = student_data.get_transaction_history_with_time()[::-1]

        context = {
            'first_name': request.user.studentdata.first_name,
            'student_data': student_data,
            'transaction_history': transaction_history,  # Pass transaction history data with times
        }

        if request.method == 'POST':
            # Process transaction form submission
            transaction_amount = request.POST.get('transaction-amount')
            transaction_category = request.POST.get('transaction-category')
            transaction_note = request.POST.get('transaction-note')

            if not transaction_amount:
                messages.error(request, "Transaction amount cannot be empty.")
            else:
                transaction_amount = Decimal(transaction_amount)
                if transaction_amount < 1:
                    messages.error(request, "Transaction amount must be at least 1 Rupee.")
                elif transaction_amount > student_data.balance:
                    messages.error(request, "Insufficient balance for the transaction.")
                else:
                    student_data.add_transaction(transaction_amount, transaction_category, transaction_note)
                    student_data.balance -= transaction_amount
                    student_data.save()
                    messages.success(request, f"Transaction successful of {transaction_amount} Rupees.")

                    # Redirect back to the same page (refresh the page)
                    return HttpResponseRedirect(reverse('welcome'))

        return render(request, 'welcome.html', context)
    else:
        return redirect('/login/')

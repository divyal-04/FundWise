from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ParentProfile
from django.contrib.auth import authenticate, login, logout
from .helpers import send_forget_password_mail
import uuid





def parent_forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'No user found with this username.')
                return redirect('parent_forgot_password')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = ParentProfile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email has been sent.')
            return redirect('parent_forgot_password')

    except Exception as e:
        print(e)

    return render(request, 'parent/parent_forget_password.html')

from django.contrib import messages

def parent_change_password(request, token):
    context = {}

    try:
        profile_obj = ParentProfile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.error(request, 'No user id found.')
                return redirect(f'parent_change_password/{token}/')

            if new_password != confirm_password:
                messages.error(request, 'Password does not match!')
                return redirect(f'/parent/change_password/{token}/')


            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('parent_login')

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred.')
    return render(request, 'parent/parent_change_password.html', context)


from django.contrib.auth.models import User

from django.contrib.auth import login

def parent_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        child_username = request.POST.get('child_username')
        parent_first_name = request.POST.get('parent_first_name')
        parent_last_name = request.POST.get('parent_last_name')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('parent_register')

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken.')
                return redirect('parent_register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken.')
                return redirect('parent_register')

            # Check if a user with the child username exists
            try:
                child_user = User.objects.get(username=child_username)
            except User.DoesNotExist:
                messages.error(request, 'No child with that  username exists.')
                return redirect('parent_register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            # Create ParentProfile with additional fields and connect child and parent
            ParentProfile.objects.create(
                user=user_obj,
                child_username=child_username,
                parent_first_name=parent_first_name,
                parent_last_name=parent_last_name,
            )

            # Log in the user after registration
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            # Redirect to the login page after successful registration
            return redirect('parent_login')

        except Exception as e:
            print(e)

    return render(request, 'parent/parent_register.html')

def parent_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both Username and Password are required.')
            return redirect('parent_login')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect('parent_login')

        login(request, user)
        return redirect('parent_dashboard')  # Redirect to the parent home page

    return render(request, 'parent/parent_login.html')

from django.shortcuts import render, redirect
from accounts.models import StudentData
from parent.models import ParentProfile
from django.db.models import F
from decimal import Decimal, DecimalException
from django.contrib import messages

def parent_dashboard(request):
    if request.user.is_authenticated:
        try:
            parent_profile = ParentProfile.objects.get(user=request.user)
            parent_first_name = parent_profile.parent_first_name
            child_username = parent_profile.child_username

            try:
                child_data = StudentData.objects.get(user__username=child_username)

                if request.method == 'POST':
                    # Check if money is being added to the parent's wallet
                    add_to_wallet = request.POST.get('add_to_wallet')
                    if add_to_wallet:
                        try:
                            amount_to_add = Decimal(add_to_wallet)
                            if amount_to_add > 0:
                                # Use F() expression to update parent_wallet
                                ParentProfile.objects.filter(user=request.user).update(parent_wallet=F('parent_wallet') + amount_to_add)
                                messages.success(request, f"{amount_to_add} Rupees added to your wallet.")
                            else:
                                messages.error(request, "Amount must be greater than zero.")
                        except DecimalException:
                            messages.error(request, "Invalid amount.")

                    # Check if money is being added to the child's wallet
                    add_to_child_wallet = request.POST.get('add_to_child_wallet')
                    if add_to_child_wallet:
                        try:
                            amount_to_add = Decimal(add_to_child_wallet)
                            if amount_to_add > 0:
                                parent_wallet = ParentProfile.objects.get(user=request.user)
                                child_data = StudentData.objects.get(user__username=child_username)

                                if parent_wallet.parent_wallet >= amount_to_add:
                                    # Deduct from the parent's wallet using F() expression
                                    ParentProfile.objects.filter(user=request.user).update(parent_wallet=F('parent_wallet') - amount_to_add)

                                    # Add to the child's wallet
                                    child_data.balance += amount_to_add
                                    child_data.save()

                                    messages.success(request, f"{amount_to_add} Rupees added to your childs wallet.")
                                else:
                                    messages.error(request, "Insufficient balance in your wallet.")
                            else:
                                messages.error(request, "Amount must be greater than zero.")
                        except DecimalException:
                            messages.error(request, "Invalid amount.")

                transaction_history = child_data.get_transaction_history_with_time()[::-1]
                wallet_balance = child_data.balance

                all_messages = messages.get_messages(request)

                return render(request, 'parent/dashboard.html', {
                    'parent_first_name': parent_first_name,
                    'child_username': child_username,
                    'transaction_history': transaction_history,
                    'wallet_balance': wallet_balance,
                    'parent_wallet': ParentProfile.objects.get(user=request.user).parent_wallet,
                    'all_messages': all_messages,
                })

            except StudentData.DoesNotExist:
                return render(request, 'parent/dashboard.html', {
                    'parent_first_name': parent_first_name,
                    'child_username': child_username,
                    'transaction_history': [],
                    'wallet_balance': 0.00,
                })

        except ParentProfile.DoesNotExist:
            return redirect('parent_login')

    return redirect('parent_login')














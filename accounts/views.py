
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomPasswordChangeForm

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard view (admin and user)
@login_required
def dashboard(request):
    if request.user.role == CustomUser.ADMIN:
        users = CustomUser.objects.all()  # Admin sees all users
        return render(request, 'accounts/admin_dashboard.html', {'users': users})
    return render(request, 'accounts/user_dashboard.html')

# User registration view (admin can add users)
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration

            # Redirect to the login page after registration
            messages.success(request, 'Registration successful. Please log in.')  # Optional success message
            return redirect('login')  # Redirect to login page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register_user.html', {'form': form})

# Password change view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()  # This saves the new password
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

# Delete user view
@login_required
def delete_user(request, user_id):
    if request.user.role == CustomUser.ADMIN:  # Ensure only admins can delete users
        user = get_object_or_404(CustomUser, id=user_id)
        if user.id != request.user.id:  # Prevent self-deletion
            user.delete()
            messages.success(request, 'User deleted successfully.')
        else:
            messages.error(request, 'You cannot delete your own account.')
    else:
        messages.error(request, 'Unauthorized action.')
    return redirect('dashboard')

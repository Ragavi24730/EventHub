from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ParticipantProfileForm, OrganizerProfileForm
from .models import ParticipantProfile, OrganizerProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            role = form.cleaned_data.get('role')
            if role == 'organizer':
                OrganizerProfile.objects.create(
                    user=user,
                    organization_name=form.cleaned_data.get('organization_name'),
                    phone=form.cleaned_data.get('phone', '')
                )
                messages.success(request, f"Organizer account created successfully for {user.username}! Please log in.")
            else:
                ParticipantProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data.get('phone', '')
                )
                messages.success(request, f"Participant account created successfully for {user.username}! Please log in.")

            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_organizer_user:
            return redirect('organizer_dashboard')
        return redirect('participant_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                if user.is_organizer_user:
                    return redirect('organizer_dashboard')
                return redirect('participant_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    
    if hasattr(user, 'organizer_profile'):
        profile = user.organizer_profile
        profile_form = OrganizerProfileForm(instance=profile)
        is_organizer = True
    else:
        profile, created = ParticipantProfile.objects.get_or_create(user=user)
        profile_form = ParticipantProfileForm(instance=profile)
        is_organizer = False

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if is_organizer:
            profile_form = OrganizerProfileForm(request.POST, instance=profile)
        else:
            profile_form = ParticipantProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below.")

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_organizer': is_organizer,
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)

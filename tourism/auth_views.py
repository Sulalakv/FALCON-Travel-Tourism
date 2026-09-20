from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import Booking, UserProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Profile phone number update
            phone = form.cleaned_data.get('phone_number')
            if phone and hasattr(user, 'profile'):
                user.profile.phone_number = phone
                user.profile.save()

            login(request, user)
            messages.success(request, f"Welcome to Falcon Travel, {user.first_name or user.username}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below to register your account.")
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', '')

    if next_url and not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ''

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Support login with either username or email address
            user = None
            if '@' in username_or_email:
                try:
                    matched_user = User.objects.get(email__iexact=username_or_email)
                    user = authenticate(request, username=matched_user.username, password=password)
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    pass

            if user is None:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect(next_url or 'home')
            else:
                messages.error(request, "Invalid username/email or password.")
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update User fields
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()

            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors in the profile form.")
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial_data)

    user_bookings = Booking.objects.filter(user=request.user)
    context = {
        'form': form,
        'profile': profile,
        'total_bookings': user_bookings.count(),
        'confirmed_bookings': user_bookings.filter(status='confirmed').count(),
    }
    return render(request, 'auth/profile.html', context)


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    status_filter = request.GET.get('status', '').strip()

    if status_filter in ['pending', 'confirmed', 'completed', 'cancelled']:
        bookings = bookings.filter(status=status_filter)

    context = {
        'bookings': bookings,
        'current_status': status_filter,
        'total_count': Booking.objects.filter(user=request.user).count(),
        'pending_count': Booking.objects.filter(user=request.user, status='pending').count(),
        'confirmed_count': Booking.objects.filter(user=request.user, status='confirmed').count(),
        'cancelled_count': Booking.objects.filter(user=request.user, status='cancelled').count(),
    }
    return render(request, 'auth/my_bookings.html', context)


@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status in ['completed', 'cancelled']:
        messages.warning(request, f"Booking #{booking.booking_code} cannot be cancelled as it is already {booking.status}.")
        return redirect('my_bookings')

    if request.method == 'POST':
        reason = request.POST.get('cancellation_reason', 'Cancelled by user.')
        booking.status = 'cancelled'
        booking.cancellation_reason = reason
        booking.save()
        messages.success(request, f"Booking #{booking.booking_code} for {booking.destination or booking.package} has been cancelled.")
        return redirect('my_bookings')

    return render(request, 'auth/cancel_confirm.html', {'booking': booking})

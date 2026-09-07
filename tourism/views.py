from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Destination, Package, Booking, ContactMessage, Guide, Service, NewsletterSubscriber
from .forms import BookingForm, ContactForm, NewsletterForm

def home_view(request):
    destinations = Destination.objects.all()
    popular_destinations = Destination.objects.filter(is_popular=True)
    packages = Package.objects.filter(is_featured=True)
    guides = Guide.objects.all()
    services = Service.objects.all()
    
    where_to = request.GET.get('where_to', '').strip()
    destination_select = request.GET.get('destination_select', '').strip()
    duration = request.GET.get('duration', '').strip()
    
    filtered_packages = packages
    is_searched = False
    
    if where_to or (destination_select and destination_select != 'destination') or (duration and duration != 'duration'):
        is_searched = True
        filtered_packages = Package.objects.all()
        
        if where_to:
            filtered_packages = filtered_packages.filter(destination__name__icontains=where_to)
        elif destination_select and destination_select != 'destination':
            filtered_packages = filtered_packages.filter(destination__name__iexact=destination_select)
            
        if duration and duration != 'duration':
            if duration == 'day-1':
                filtered_packages = filtered_packages.filter(duration__icontains='1')
            elif duration == '2-4 days':
                filtered_packages = filtered_packages.filter(duration__icontains='2') | filtered_packages.filter(duration__icontains='3') | filtered_packages.filter(duration__icontains='4')
            elif duration == '5-7 days':
                filtered_packages = filtered_packages.filter(duration__icontains='5') | filtered_packages.filter(duration__icontains='6') | filtered_packages.filter(duration__icontains='7')
            elif duration == '7+ days':
                filtered_packages = filtered_packages.filter(duration__icontains='7') | filtered_packages.filter(duration__icontains='8') | filtered_packages.filter(duration__icontains='10') | filtered_packages.filter(duration__icontains='14')

    context = {
        'destinations': destinations,
        'popular_destinations': popular_destinations,
        'packages': filtered_packages,
        'guides': guides,
        'services': services,
        'is_searched': is_searched,
        'search_where_to': where_to,
        'search_destination': destination_select,
        'search_duration': duration,
    }
    return render(request, 'index.html', context)


def about_view(request):
    guides = Guide.objects.all()
    context = {
        'guides': guides
    }
    return render(request, 'about.html', context)


def packages_view(request):
    packages = Package.objects.all()
    context = {
        'packages': packages
    }
    return render(request, 'packages.html', context)


def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            messages.success(request, f"Thank you, {booking.name}! Your booking #{booking.booking_code} for {booking.destination or booking.package} (${booking.total_price}) has been received successfully.")
            if request.user.is_authenticated:
                return redirect('my_bookings')
            return redirect('booking')
        else:
            messages.error(request, "Failed to submit booking request. Please verify the required fields.")
    else:
        initial_data = {}
        dest_id = request.GET.get('dest')
        pkg_id = request.GET.get('pkg')

        if request.user.is_authenticated:
            initial_data['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['email'] = request.user.email

        if pkg_id:
            try:
                pkg = Package.objects.get(id=pkg_id)
                initial_data['package'] = pkg
                if pkg.destination:
                    initial_data['destination'] = pkg.destination
            except Package.DoesNotExist:
                pass
        elif dest_id:
            try:
                dest = Destination.objects.get(id=dest_id)
                initial_data['destination'] = dest
            except Destination.DoesNotExist:
                pass

        form = BookingForm(initial=initial_data)
        
    context = {
        'form': form,
        'packages': Package.objects.all(),
        'destinations': Destination.objects.all(),
    }
    return render(request, 'booking.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f"Thank you {contact.name}! Your message has been sent successfully. We will get back to you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Failed to send message. Please verify input fields.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['email'] = request.user.email
            if hasattr(request.user, 'profile') and request.user.profile.phone_number:
                initial_data['phone'] = request.user.profile.phone_number
        form = ContactForm(initial=initial_data)
        
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def newsletter_subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing to Falcon Travel newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter!")
        else:
            messages.error(request, "Please provide a valid email address.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

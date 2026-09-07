from django.contrib import admin
from .models import Destination, Package, Booking, ContactMessage, NewsletterSubscriber, Guide, Service, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'passport_number', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'description')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'duration', 'price', 'max_slots', 'available_slots', 'is_featured', 'destination')
    list_filter = ('is_featured', 'destination')
    search_fields = ('title', 'location', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'name', 'email', 'package', 'destination', 'num_guests', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'destination', 'created_at')
    search_fields = ('booking_code', 'name', 'email', 'special_request', 'cancellation_reason')
    readonly_fields = ('booking_code', 'total_price', 'created_at', 'updated_at')
    actions = ['mark_confirmed', 'mark_cancelled', 'mark_completed']

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')

    @admin.action(description="Mark selected bookings as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

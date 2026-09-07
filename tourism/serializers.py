from django.contrib.auth.models import User
from .models import Destination, Package, Booking, UserProfile

# Try importing DRF serializers, with clean fallback
try:
    from rest_framework import serializers

    class UserProfileSerializer(serializers.ModelSerializer):
        avatar_url = serializers.ReadOnlyField()

        class Meta:
            model = UserProfile
            fields = ['phone_number', 'avatar', 'avatar_url', 'address', 'bio', 'passport_number', 'created_at']


    class UserSerializer(serializers.ModelSerializer):
        profile = UserProfileSerializer(read_only=True)

        class Meta:
            model = User
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


    class DestinationSerializer(serializers.ModelSerializer):
        image_url = serializers.ReadOnlyField()

        class Meta:
            model = Destination
            fields = ['id', 'name', 'description', 'image', 'image_url', 'is_popular']


    class PackageSerializer(serializers.ModelSerializer):
        image_url = serializers.ReadOnlyField(source='get_image_url')
        destination_name = serializers.ReadOnlyField(source='destination.name')
        available_slots = serializers.ReadOnlyField()
        booked_slots = serializers.ReadOnlyField()

        class Meta:
            model = Package
            fields = [
                'id', 'title', 'description', 'location', 'duration',
                'destination', 'destination_name', 'price', 'max_slots',
                'available_slots', 'booked_slots', 'is_featured', 'image_url'
            ]


    class BookingSerializer(serializers.ModelSerializer):
        package_details = PackageSerializer(source='package', read_only=True)
        destination_name = serializers.ReadOnlyField(source='destination.name')

        class Meta:
            model = Booking
            fields = [
                'id', 'booking_code', 'user', 'package', 'package_details',
                'destination', 'destination_name', 'name', 'email',
                'num_guests', 'total_price', 'date_time', 'status',
                'special_request', 'cancellation_reason', 'created_at', 'updated_at'
            ]
            read_only_fields = ['id', 'booking_code', 'user', 'total_price', 'created_at', 'updated_at']

except ImportError:
    # DRF fallback dummy classes if not installed
    class UserProfileSerializer: pass
    class UserSerializer: pass
    class DestinationSerializer: pass
    class PackageSerializer: pass
    class BookingSerializer: pass

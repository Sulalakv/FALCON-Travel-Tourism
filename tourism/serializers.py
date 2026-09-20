from django.contrib.auth.models import User
from .models import Destination, Package, Booking, UserProfile

# Try importing DRF serializers, with clean fallback
try:
    from rest_framework import serializers

    class UserProfileSerializer(serializers.ModelSerializer):
        avatar_url = serializers.ReadOnlyField()

        class Meta:
            model = UserProfile
            fields = [
                'phone_number',
                'avatar',
                'avatar_url',
                'address',
                'bio',
                'passport_number',
                'created_at'
            ]
            extra_kwargs = {
                'passport_number': {'write_only': True},
            }


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

        def validate_num_guests(self, value):
            if value < 1:
                raise serializers.ValidationError(
                    "Number of guests must be at least 1."
            )

            if value > 20:
                raise serializers.ValidationError(
                    "Number of guests cannot exceed 20."
            )

            return value

        def validate(self, attrs):
            package = attrs.get('package')
            num_guests = attrs.get('num_guests', 1)

            if not package:
               raise serializers.ValidationError({
                    'package': 'A package is required for booking.'
                })

            if num_guests > package.available_slots:
                raise serializers.ValidationError({
                      'num_guests': (
                          f'Only {package.available_slots} slot(s) are available '
                          f'for this package.'
                        )
                })

            return attrs

        class Meta:
            model = Booking
            fields = [
                'id', 'booking_code', 'user', 'package', 'package_details',
                'destination', 'destination_name', 'name', 'email',
                'num_guests', 'total_price', 'date_time', 'status',
                'special_request', 'cancellation_reason', 'created_at', 'updated_at'
            ]
            read_only_fields = [
                'id',
                'booking_code',
                'user',
                'total_price',
                'status',
                'cancellation_reason',
                'created_at',
                'updated_at'
            ]

except ImportError:
    # DRF fallback dummy classes if not installed
    class UserProfileSerializer: pass
    class UserSerializer: pass
    class DestinationSerializer: pass
    class PackageSerializer: pass
    class BookingSerializer: pass

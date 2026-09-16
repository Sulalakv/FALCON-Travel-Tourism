from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Destination, Package, Booking, UserProfile

try:
    from rest_framework import generics, permissions, status
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from .serializers import DestinationSerializer, PackageSerializer, BookingSerializer, UserSerializer, UserProfileSerializer

    class DestinationListAPIView(generics.ListAPIView):
        queryset = Destination.objects.all()
        serializer_class = DestinationSerializer
        permission_classes = [permissions.AllowAny]


    class DestinationDetailAPIView(generics.RetrieveAPIView):
        queryset = Destination.objects.all()
        serializer_class = DestinationSerializer
        permission_classes = [permissions.AllowAny]


    class PackageListAPIView(generics.ListAPIView):
        serializer_class = PackageSerializer
        permission_classes = [permissions.AllowAny]

        def get_queryset(self):
            queryset = Package.objects.all()
            dest = self.request.query_params.get('destination')
            search = self.request.query_params.get('search')
            if dest:
                queryset = queryset.filter(destination__name__icontains=dest)
            if search:
                queryset = queryset.filter(title__icontains=search) | queryset.filter(location__icontains=search)
            return queryset


    class PackageDetailAPIView(generics.RetrieveAPIView):
        queryset = Package.objects.all()
        serializer_class = PackageSerializer
        permission_classes = [permissions.AllowAny]


    class BookingListCreateAPIView(generics.ListCreateAPIView):
        serializer_class = BookingSerializer
        permission_classes = [permissions.IsAuthenticated]

        def get_queryset(self):
            return Booking.objects.filter(user=self.request.user)

        def perform_create(self, serializer):
            package_id = serializer.validated_data.get('package').id
            num_guests = serializer.validated_data.get('num_guests', 1)

            with transaction.atomic():
                package = (
                    Package.objects
                    .select_for_update()
                    .get(pk=package_id)
                )

            # Re-check capacity after locking the package row.
                if num_guests > package.available_slots:
                    from rest_framework.exceptions import ValidationError

                    raise ValidationError({
                        'num_guests': (
                            f'Only {package.available_slots} slot(s) are '
                            f'available for this package.'
                        )
                    })

                serializer.save(
                    user=self.request.user,
                    package=package
                )


    class BookingCancelAPIView(APIView):
        permission_classes = [permissions.IsAuthenticated]

        def post(self, request, pk):
            booking = get_object_or_404(Booking, pk=pk, user=request.user)
            if booking.status in ['cancelled', 'completed']:
                return Response(
                    {'error': f'Booking is already {booking.status}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            reason = request.data.get('cancellation_reason', 'Cancelled via API')
            booking.status = 'cancelled'
            booking.cancellation_reason = reason
            booking.save()
            return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)


    class UserProfileAPIView(APIView):
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        def put(self, request):
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

except ImportError:
    # Standard JsonResponse fallback if DRF is not installed in local environment
    def DestinationListAPIView(request):
        destinations = list(Destination.objects.values('id', 'name', 'description', 'is_popular'))
        return JsonResponse({'destinations': destinations})

    def DestinationDetailAPIView(request, pk):
        dest = get_object_or_404(Destination, pk=pk)
        return JsonResponse({'id': dest.id, 'name': dest.name, 'description': dest.description})

    def PackageListAPIView(request):
        packages = list(Package.objects.values('id', 'title', 'location', 'price', 'max_slots'))
        return JsonResponse({'packages': packages})

    def PackageDetailAPIView(request, pk):
        pkg = get_object_or_404(Package, pk=pk)
        return JsonResponse({'id': pkg.id, 'title': pkg.title, 'location': pkg.location, 'price': str(pkg.price)})

    def BookingListCreateAPIView(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        bookings = list(Booking.objects.filter(user=request.user).values('id', 'booking_code', 'status', 'total_price'))
        return JsonResponse({'bookings': bookings})

    def BookingCancelAPIView(request, pk):
        return JsonResponse({'message': 'API view'})

    def UserProfileAPIView(request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return JsonResponse({'username': request.user.username, 'email': request.user.email})

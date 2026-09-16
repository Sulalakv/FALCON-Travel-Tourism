from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from . import auth_views
from . import api_views


urlpatterns = [
    # =========================================================
    # Main Public Pages
    # =========================================================
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('packages/', views.packages_view, name='packages'),
    path('booking/', views.booking_view, name='booking'),
    path('contact/', views.contact_view, name='contact'),
    path('newsletter/', views.newsletter_subscribe_view, name='newsletter_subscribe'),

    # =========================================================
    # User Authentication & Profiles
    # =========================================================
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('my-bookings/', auth_views.my_bookings_view, name='my_bookings'),
    path(
        'booking/cancel/<int:booking_id>/',
        auth_views.cancel_booking_view,
        name='cancel_booking'
    ),

    # =========================================================
    # JWT Authentication
    # Existing endpoints - kept for backward compatibility
    # =========================================================
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Versioned JWT endpoints
    path(
        'api/v1/token/',
        TokenObtainPairView.as_view(),
        name='v1_token_obtain_pair'
    ),
    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='v1_token_refresh'
    ),

    # =========================================================
    # REST API - Existing /api/ endpoints
    # Kept so existing clients continue to work
    # =========================================================
    path(
        'api/destinations/',
        api_views.DestinationListAPIView.as_view()
        if hasattr(api_views.DestinationListAPIView, 'as_view')
        else api_views.DestinationListAPIView,
        name='api_destinations_list'
    ),
    path(
        'api/destinations/<int:pk>/',
        api_views.DestinationDetailAPIView.as_view()
        if hasattr(api_views.DestinationDetailAPIView, 'as_view')
        else api_views.DestinationDetailAPIView,
        name='api_destinations_detail'
    ),
    path(
        'api/packages/',
        api_views.PackageListAPIView.as_view()
        if hasattr(api_views.PackageListAPIView, 'as_view')
        else api_views.PackageListAPIView,
        name='api_packages_list'
    ),
    path(
        'api/packages/<int:pk>/',
        api_views.PackageDetailAPIView.as_view()
        if hasattr(api_views.PackageDetailAPIView, 'as_view')
        else api_views.PackageDetailAPIView,
        name='api_packages_detail'
    ),
    path(
        'api/bookings/',
        api_views.BookingListCreateAPIView.as_view()
        if hasattr(api_views.BookingListCreateAPIView, 'as_view')
        else api_views.BookingListCreateAPIView,
        name='api_bookings_list'
    ),
    path(
        'api/bookings/<int:pk>/cancel/',
        api_views.BookingCancelAPIView.as_view()
        if hasattr(api_views.BookingCancelAPIView, 'as_view')
        else api_views.BookingCancelAPIView,
        name='api_bookings_cancel'
    ),
    path(
        'api/profile/',
        api_views.UserProfileAPIView.as_view()
        if hasattr(api_views.UserProfileAPIView, 'as_view')
        else api_views.UserProfileAPIView,
        name='api_user_profile'
    ),

    # =========================================================
    # REST API - Version 1
    # =========================================================
    path(
        'api/v1/destinations/',
        api_views.DestinationListAPIView.as_view()
        if hasattr(api_views.DestinationListAPIView, 'as_view')
        else api_views.DestinationListAPIView,
        name='v1_api_destinations_list'
    ),
    path(
        'api/v1/destinations/<int:pk>/',
        api_views.DestinationDetailAPIView.as_view()
        if hasattr(api_views.DestinationDetailAPIView, 'as_view')
        else api_views.DestinationDetailAPIView,
        name='v1_api_destinations_detail'
    ),
    path(
        'api/v1/packages/',
        api_views.PackageListAPIView.as_view()
        if hasattr(api_views.PackageListAPIView, 'as_view')
        else api_views.PackageListAPIView,
        name='v1_api_packages_list'
    ),
    path(
        'api/v1/packages/<int:pk>/',
        api_views.PackageDetailAPIView.as_view()
        if hasattr(api_views.PackageDetailAPIView, 'as_view')
        else api_views.PackageDetailAPIView,
        name='v1_api_packages_detail'
    ),
    path(
        'api/v1/bookings/',
        api_views.BookingListCreateAPIView.as_view()
        if hasattr(api_views.BookingListCreateAPIView, 'as_view')
        else api_views.BookingListCreateAPIView,
        name='v1_api_bookings_list'
    ),
    path(
        'api/v1/bookings/<int:pk>/cancel/',
        api_views.BookingCancelAPIView.as_view()
        if hasattr(api_views.BookingCancelAPIView, 'as_view')
        else api_views.BookingCancelAPIView,
        name='v1_api_bookings_cancel'
    ),
    path(
        'api/v1/profile/',
        api_views.UserProfileAPIView.as_view()
        if hasattr(api_views.UserProfileAPIView, 'as_view')
        else api_views.UserProfileAPIView,
        name='v1_api_user_profile'
    ),


    # Swagger/OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/v1/schema/', SpectacularAPIView.as_view(), name='v1-schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='v1-schema'), name='v1-swagger-ui'),
]
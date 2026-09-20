from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Booking, Destination, Package


class BookingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser',
            password='TestPassword123!'
        )

        self.destination = Destination.objects.create(
            name='Test Destination',
            description='Test destination'
        )

        self.package = Package.objects.create(
            title='Test Package',
            description='Test package description',
            location='Test Location',
            duration='2 days',
            destination=self.destination,
            price=450.00,
            max_slots=20
        )

        self.valid_booking_data = {
            'package': self.package.id,
            'name': 'Test User',
            'email': 'test@example.com',
            'num_guests': 2,
            'date_time': '2026-10-01 10:00',
            'special_request': 'Test booking'
        }

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_user_cannot_create_booking(self):
        response = self.client.post(
            '/api/v1/bookings/',
            self.valid_booking_data,
            format='json'
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Booking.objects.count(), 0)

    def test_authenticated_user_can_create_booking(self):
        self.authenticate()

        response = self.client.post(
            '/api/v1/bookings/',
            self.valid_booking_data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.package, self.package)
        self.assertEqual(booking.num_guests, 2)
        self.assertEqual(booking.total_price, 900.00)
        self.assertEqual(booking.status, 'pending')

    def test_booking_rejects_more_than_20_guests(self):
        self.authenticate()

        data = self.valid_booking_data.copy()
        data['num_guests'] = 21

        response = self.client.post(
            '/api/v1/bookings/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('num_guests', response.data)
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_rejects_zero_guests(self):
        self.authenticate()

        data = self.valid_booking_data.copy()
        data['num_guests'] = 0

        response = self.client.post(
            '/api/v1/bookings/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('num_guests', response.data)
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_rejects_when_capacity_is_insufficient(self):
        self.authenticate()

        Booking.objects.create(
            user=self.user,
            package=self.package,
            name='Existing User',
            email='existing@example.com',
            num_guests=19,
            date_time='2026-09-30 10:00'
        )

        data = self.valid_booking_data.copy()
        data['num_guests'] = 2

        response = self.client.post(
            '/api/v1/bookings/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('num_guests', response.data)

    def test_user_can_only_see_own_bookings(self):
        self.authenticate()

        Booking.objects.create(
            user=self.user,
            package=self.package,
            name='My Booking',
            email='my@example.com',
            num_guests=1,
            date_time='2026-10-01 10:00'
        )

        other_user = User.objects.create_user(
            username='otheruser',
            password='OtherPassword123!'
        )

        Booking.objects.create(
            user=other_user,
            package=self.package,
            name='Other Booking',
            email='other@example.com',
            num_guests=1,
            date_time='2026-10-02 10:00'
        )

        response = self.client.get('/api/v1/bookings/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'My Booking')

    def test_user_can_cancel_own_booking(self):
        self.authenticate()

        booking = Booking.objects.create(
            user=self.user,
            package=self.package,
            name='Cancel Test',
            email='cancel@example.com',
            num_guests=1,
            date_time='2026-10-01 10:00'
        )

        response = self.client.post(
            f'/api/v1/bookings/{booking.id}/cancel/',
            {'cancellation_reason': 'Testing cancellation'},
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        booking.refresh_from_db()

        self.assertEqual(booking.status, 'cancelled')
        self.assertEqual(
            booking.cancellation_reason,
            'Testing cancellation'
        )

    def test_user_cannot_cancel_another_users_booking(self):
        self.authenticate()

        other_user = User.objects.create_user(
            username='otheruser',
            password='OtherPassword123!'
        )

        booking = Booking.objects.create(
            user=other_user,
            package=self.package,
            name='Other User',
            email='other@example.com',
            num_guests=1,
            date_time='2026-10-02 10:00'
        )

        response = self.client.post(
            f'/api/v1/bookings/{booking.id}/cancel/',
            {'cancellation_reason': 'Unauthorized attempt'},
            format='json'
        )

        self.assertEqual(response.status_code, 404)

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'pending')


    def test_user_cannot_assign_booking_to_another_user(self):
        self.authenticate()

        other_user = User.objects.create_user(
            username='otheruser',
            password='OtherPassword123!'
        )

        data = self.valid_booking_data.copy()
        data['user'] = other_user.id

        response = self.client.post(
            '/api/v1/bookings/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        booking = Booking.objects.first()

        self.assertEqual(booking.user, self.user)
        self.assertNotEqual(booking.user, other_user)


    def test_user_cannot_change_booking_status_during_creation(self):
        self.authenticate()

        data = self.valid_booking_data.copy()
        data['status'] = 'completed'

        response = self.client.post(
            '/api/v1/bookings/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        booking = Booking.objects.first()

        self.assertEqual(booking.status, 'pending')
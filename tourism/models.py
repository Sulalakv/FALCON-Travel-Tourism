import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return None

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance)


class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        name_lower = self.name.lower()
        if 'australia' in name_lower:
            return static('public/australia.jpg')
        elif 'bangkok' in name_lower:
            return static('public/bangkok.jpg')
        elif 'istanbul' in name_lower:
            return static('public/istanbul 1.jpg')
        elif 'thailand' in name_lower:
            return static('public/thailand.jpg')
        elif 'greece' in name_lower:
            return static('public/box1.jpg')
        elif 'london' in name_lower:
            return static('public/box2.jpg')
        elif 'maldives' in name_lower:
            return static('public/box3.jpg')
        elif 'paris' in name_lower:
            return static('public/box4.jpg')
        return static('public/australia.jpg')


class Package(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    duration = models.CharField(max_length=100, help_text="e.g. 1- Day Tour, 2-4 Days Tour, etc.")
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='packages')
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    image_class = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. img-1, img-2 for stylesheet fallbacks")
    is_featured = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    max_slots = models.PositiveIntegerField(default=20, help_text="Total available capacity per tour")

    def __str__(self):
        return f"{self.title} ({self.location}) - ${self.price}"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        cls = self.image_class or ""
        if 'img-1' in cls:
            return static('public/cruise-1578528_1280.jpg')
        elif 'img-2' in cls:
            return static('public/island-3542290_1280.jpg')
        elif 'img-3' in cls:
            return static('public/mountains-190055_1280.jpg')
        elif 'img-4' in cls:
            return static('public/hallstatt-3609863_1280.jpg')
        elif 'img-5' in cls:
            return static('public/sunrise-1014713_1280.jpg')
        return static('public/thailand.jpg')

    @property
    def booked_slots(self):
        active_bookings = self.bookings.exclude(status='cancelled')
        return sum(b.num_guests for b in active_bookings)

    @property
    def available_slots(self):
        return max(0, self.max_slots - self.booked_slots)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_code = models.CharField(max_length=30, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date_time = models.CharField(max_length=100, help_text="Date and time string from datetimepicker")
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    num_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_request = models.TextField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.booking_code or self.id} ({self.name} - {self.status})"

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"FLC-{uuid.uuid4().hex[:6].upper()}"
        
        # Calculate dynamic price
        if self.package and self.package.price:
            self.total_price = Decimal(str(self.package.price)) * Decimal(str(self.num_guests or 1))
        elif not self.total_price:
            self.total_price = Decimal("100.00") * Decimal(str(self.num_guests or 1))

        if self.package and not self.destination:
            self.destination = self.package.destination

        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Guide(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='guides/', blank=True, null=True)
    image_static = models.CharField(max_length=100, default='img/team-1.jpg')
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return static(self.image_static)


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_static = models.CharField(max_length=100, default='public/service-1.jpg')

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return static(self.image_static)

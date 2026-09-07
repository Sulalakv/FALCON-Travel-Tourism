import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from tourism.models import Destination, Package, Guide, Service

print("Starting safe database seeding...")

# ---------------------------------------------------------
# DESTINATIONS
# ---------------------------------------------------------
print("Creating/updating Destinations...")

greece, _ = Destination.objects.update_or_create(
    name="Greece",
    defaults={
        "description": "Explore beautiful beaches and ancient history.",
        "is_popular": True,
    }
)

london, _ = Destination.objects.update_or_create(
    name="London",
    defaults={
        "description": "Visit the iconic Big Ben, and the London Eye.",
        "is_popular": True,
    }
)

maldives, _ = Destination.objects.update_or_create(
    name="Maldives",
    defaults={
        "description": "Enjoy luxury resorts and azure crystal waters.",
        "is_popular": True,
    }
)

paris, _ = Destination.objects.update_or_create(
    name="Paris",
    defaults={
        "description": "The city of lights, romance, and incredible food.",
        "is_popular": True,
    }
)

thailand, _ = Destination.objects.update_or_create(
    name="Thailand",
    defaults={
        "description": "Vibrant street life, exotic beaches and ornate temples.",
        "is_popular": True,
    }
)


# ---------------------------------------------------------
# PACKAGES
# ---------------------------------------------------------
print("Creating/updating Packages...")

Package.objects.update_or_create(
    title="Hawak Escape",
    defaults={
        "description": "Explore the beauty of the island for three days and 2 nights with private guide.",
        "location": "Greece",
        "duration": "2-4 days",
        "destination": greece,
        "image_class": "img-1",
        "is_featured": True,
        "price": 450.00,
    }
)

Package.objects.update_or_create(
    title="London Heritage",
    defaults={
        "description": "Immerse yourself in royal history and London culture across 5 golden days.",
        "location": "United Kingdom",
        "duration": "5-7 days",
        "destination": london,
        "image_class": "img-2",
        "is_featured": True,
        "price": 590.00,
    }
)

Package.objects.update_or_create(
    title="Parisian Romance",
    defaults={
        "description": "Experience the Eiffel tower, Louvre museum, and world class culinary delights.",
        "location": "France",
        "duration": "5-7 days",
        "destination": paris,
        "image_class": "img-3",
        "is_featured": True,
        "price": 750.00,
    }
)

Package.objects.update_or_create(
    title="Siam Wonders",
    defaults={
        "description": "Vibrant night markets, exotic beaches, and majestic temple architecture.",
        "location": "Thailand",
        "duration": "2-4 days",
        "destination": thailand,
        "image_class": "img-4",
        "is_featured": True,
        "price": 320.00,
    }
)

Package.objects.update_or_create(
    title="Maldives Paradise",
    defaults={
        "description": "Overwater villa luxury stay with complimentary island cruise and snorkeling.",
        "location": "Maldives",
        "duration": "7+ days",
        "destination": maldives,
        "image_class": "img-5",
        "is_featured": True,
        "price": 690.00,
    }
)


# ---------------------------------------------------------
# GUIDES
# ---------------------------------------------------------
print("Creating/updating Guides...")

Guide.objects.update_or_create(
    name="John Doe",
    defaults={
        "role": "Senior Expedition Coordinator",
        "image_static": "img/team-1.jpg",
    }
)

Guide.objects.update_or_create(
    name="Jane Smith",
    defaults={
        "role": "Cultural Liaison Expert",
        "image_static": "img/team-2.jpg",
    }
)

Guide.objects.update_or_create(
    name="Alex Johnson",
    defaults={
        "role": "Wilderness Survival Specialist",
        "image_static": "img/team-3.jpg",
    }
)

Guide.objects.update_or_create(
    name="Sarah Brown",
    defaults={
        "role": "Lead Photographer & Instructor",
        "image_static": "img/team-4.jpg",
    }
)


# ---------------------------------------------------------
# SERVICES
# ---------------------------------------------------------
print("Creating/updating Services...")

Service.objects.update_or_create(
    title="Cruise Ticket",
    defaults={
        "description": "Enjoy world-class amenities and stunning views with Falcon cruise lines. Book your cruise now.",
        "image_static": "public/service-1.jpg",
    }
)

Service.objects.update_or_create(
    title="Car Booking",
    defaults={
        "description": "Affordable rates, no hidden costs. Best rental vehicle deals with daily dropoff options.",
        "image_static": "public/service-2.jpg",
    }
)

Service.objects.update_or_create(
    title="Air Ticket",
    defaults={
        "description": "Enjoy world-class flight amenities and global routes with Falcon partner airlines.",
        "image_static": "public/service-3.jpg",
    }
)

Service.objects.update_or_create(
    title="Hotel Booking",
    defaults={
        "description": "Affordable rates and 5-star hotel luxury bundles. Find hotels at guaranteed low prices.",
        "image_static": "public/service-4.jpg",
    }
)

print("Database seeded successfully!")
print("Destinations, Packages, Guides, and Services are ready.")
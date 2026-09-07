import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_agency.settings')
django.setup()

from tourism.models import Destination, Package, Guide, Service

print("Clearing existing records...")
Destination.objects.all().delete()
Package.objects.all().delete()
Guide.objects.all().delete()
Service.objects.all().delete()

print("Creating Destinations...")
greece = Destination.objects.create(name="Greece", description="Explore beautiful beaches and ancient history.", is_popular=True)
london = Destination.objects.create(name="London", description="Visit the iconic Big Ben, and the London Eye.", is_popular=True)
maldives = Destination.objects.create(name="Maldives", description="Enjoy luxury resorts and azure crystal waters.", is_popular=True)
paris = Destination.objects.create(name="Paris", description="The city of lights, romance, and incredible food.", is_popular=True)
thailand = Destination.objects.create(name="Thailand", description="Vibrant street life, exotic beaches and ornate temples.", is_popular=True)

print("Creating Packages...")
Package.objects.create(
    title="Hawak Escape",
    description="Explore the beauty of the island for three days and 2 nights with private guide.",
    location="Greece",
    duration="2-4 days",
    destination=greece,
    image_class="img-1",
    is_featured=True,
    price=450.00
)

Package.objects.create(
    title="London Heritage",
    description="Immerse yourself in royal history and London culture across 5 golden days.",
    location="United Kingdom",
    duration="5-7 days",
    destination=london,
    image_class="img-2",
    is_featured=True,
    price=590.00
)

Package.objects.create(
    title="Parisian Romance",
    description="Experience the Eiffel tower, Louvre museum, and world class culinary delights.",
    location="France",
    duration="5-7 days",
    destination=paris,
    image_class="img-3",
    is_featured=True,
    price=750.00
)

Package.objects.create(
    title="Siam Wonders",
    description="Vibrant night markets, exotic beaches, and majestic temple architecture.",
    location="Thailand",
    duration="2-4 days",
    destination=thailand,
    image_class="img-4",
    is_featured=True,
    price=320.00
)

Package.objects.create(
    title="Maldives Paradise",
    description="Overwater villa luxury stay with complimentary island cruise and snorkeling.",
    location="Maldives",
    duration="7+ days",
    destination=maldives,
    image_class="img-5",
    is_featured=True,
    price=690.00
)

print("Creating Guides...")
Guide.objects.create(
    name="John Doe",
    role="Senior Expedition Coordinator",
    image_static="img/team-1.jpg"
)
Guide.objects.create(
    name="Jane Smith",
    role="Cultural Liaison Expert",
    image_static="img/team-2.jpg"
)
Guide.objects.create(
    name="Alex Johnson",
    role="Wilderness Survival Specialist",
    image_static="img/team-3.jpg"
)
Guide.objects.create(
    name="Sarah Brown",
    role="Lead Photographer & Instructor",
    image_static="img/team-4.jpg"
)

print("Creating Services...")
Service.objects.create(
    title="Cruise Ticket",
    description="Enjoy world-class amenities and stunning views with Falcon cruise lines. Book your cruise now.",
    image_static="public/service-1.jpg"
)
Service.objects.create(
    title="Car Booking",
    description="Affordable rates, no hidden costs. Best rental vehicle deals with daily dropoff options.",
    image_static="public/service-2.jpg"
)
Service.objects.create(
    title="Air Ticket",
    description="Enjoy world-class flight amenities and global routes with Falcon partner airlines.",
    image_static="public/service-3.jpg"
)
Service.objects.create(
    title="Hotel Booking",
    description="Affordable rates and 5-star hotel luxury bundles. Find hotels at guaranteed low prices.",
    image_static="public/service-4.jpg"
)

print("Database seeded successfully with dynamic Destinations, Packages, Guides, and Services!")


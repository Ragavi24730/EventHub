from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from accounts.models import ParticipantProfile, OrganizerProfile
from events.models import Category, Event
from registrations.models import Registration, Ticket
from registrations.utils import generate_unique_ticket_id, create_ticket_qr_code

class EventHubSystemTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Category
        self.category = Category.objects.create(name="Tech & AI", icon_name="laptop-code")

        # Create Organizer
        self.organizer_user = User.objects.create_user(username='org_user', password='password123')
        self.organizer_profile = OrganizerProfile.objects.create(
            user=self.organizer_user,
            organization_name="Tech Corp"
        )

        # Create Participant
        self.participant_user = User.objects.create_user(username='part_user', password='password123')
        self.participant_profile = ParticipantProfile.objects.create(user=self.participant_user)

        # Create Approved Event (capacity 2)
        self.event = Event.objects.create(
            organizer=self.organizer_user,
            category=self.category,
            title="Django Masterclass 2026",
            description="Deep dive into Django full stack.",
            date=timezone.now().date() + datetime.timedelta(days=10),
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            location="San Francisco Tech Hub",
            price=29.99,
            capacity=2,
            status='approved'
        )

    def test_seat_capacity_and_available_seats(self):
        self.assertEqual(self.event.available_seats, 2)
        self.assertFalse(self.event.is_full)

        # Register participant 1
        reg = Registration.objects.create(participant=self.participant_user, event=self.event, status='registered')
        
        self.assertEqual(self.event.registered_count, 1)
        self.assertEqual(self.event.available_seats, 1)
        self.assertFalse(self.event.is_full)

    def test_event_registration_and_ticket_generation(self):
        self.client.login(username='part_user', password='password123')
        response = self.client.post(f'/events/{self.event.slug}/register/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Registration.objects.filter(participant=self.participant_user, event=self.event).exists())
        
        reg = Registration.objects.get(participant=self.participant_user, event=self.event)
        self.assertTrue(hasattr(reg, 'ticket'))
        self.assertTrue(reg.ticket.ticket_id.startswith("EVT-2026-"))
        self.assertTrue(bool(reg.ticket.qr_code))

    def test_prevent_duplicate_registration(self):
        self.client.login(username='part_user', password='password123')
        # First registration
        self.client.post(f'/events/{self.event.slug}/register/', follow=True)
        
        # Second registration attempt
        response = self.client.post(f'/events/{self.event.slug}/register/', follow=True)
        
        # Count should still be 1
        self.assertEqual(Registration.objects.filter(participant=self.participant_user, event=self.event).count(), 1)

    def test_prevent_registration_when_event_is_full(self):
        # Fill capacity (2 seats)
        user2 = User.objects.create_user(username='user2', password='password123')
        user3 = User.objects.create_user(username='user3', password='password123')
        
        Registration.objects.create(participant=self.participant_user, event=self.event, status='registered')
        Registration.objects.create(participant=user2, event=self.event, status='registered')

        self.assertEqual(self.event.available_seats, 0)
        self.assertTrue(self.event.is_full)

        # Attempt 3rd registration by user3
        self.client.login(username='user3', password='password123')
        response = self.client.post(f'/events/{self.event.slug}/register/', follow=True)
        
        self.assertFalse(Registration.objects.filter(participant=user3, event=self.event).exists())

    def test_cancel_registration_frees_seat(self):
        reg = Registration.objects.create(participant=self.participant_user, event=self.event, status='registered')
        self.assertEqual(self.event.available_seats, 1)

        # Cancel registration
        self.client.login(username='part_user', password='password123')
        response = self.client.post(f'/registration/{reg.id}/cancel/', follow=True)

        reg.refresh_from_db()
        self.assertEqual(reg.status, 'cancelled')
        self.assertEqual(self.event.available_seats, 2) # Seat is freed!

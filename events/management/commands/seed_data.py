from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from accounts.models import ParticipantProfile, OrganizerProfile
from events.models import Category, Event
from registrations.models import Registration, Ticket
from registrations.utils import generate_unique_ticket_id, create_ticket_qr_code

class Command(BaseCommand):
    help = "Seeds initial categories, users, approved events with images, registrations, and tickets for testing."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding EventHub sample data..."))

        # 1. Categories
        categories_data = [
            {'name': 'Technology', 'icon_name': 'laptop-code', 'description': 'Cutting-edge tech, AI, software development and IT summits.'},
            {'name': 'Conference', 'icon_name': 'users', 'description': 'Keynotes, industry roundtables, leadership and networking.'},
            {'name': 'Hackathon', 'icon_name': 'code', 'description': '24-48 hour coding challenges, prize competitions and prototyping.'},
            {'name': 'Workshop', 'icon_name': 'chalkboard-user', 'description': 'Hands-on practical training, masterclasses, and skill building.'},
            {'name': 'Cultural & Music', 'icon_name': 'music', 'description': 'Concerts, art exhibitions, cultural galas, and live performances.'},
            {'name': 'Sports & Gaming', 'icon_name': 'trophy', 'description': 'Esports tournaments, marathons, and athletic meets.'},
            {'name': 'Education', 'icon_name': 'graduation-cap', 'description': 'Academic seminars, research symposiums, and career expos.'},
        ]

        categories_dict = {}
        for cat in categories_data:
            c, _ = Category.objects.get_or_create(
                name=cat['name'],
                defaults={'icon_name': cat['icon_name'], 'description': cat['description']}
            )
            categories_dict[cat['name']] = c

        # 2. Users
        # Admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@eventhub.com', 'admin123')
            admin_user.first_name = "Admin"
            admin_user.last_name = "System"
            admin_user.save()
            OrganizerProfile.objects.create(
                user=admin_user,
                organization_name="EventHub Master Admin",
                phone="+1 800-555-0100"
            )
            self.stdout.write(self.style.SUCCESS("Superuser created: admin / admin123"))

        # Organizer 1
        org1_user, created = User.objects.get_or_create(
            username='tech_org',
            defaults={'email': 'contact@globaltech.com', 'first_name': 'Tech', 'last_name': 'Events'}
        )
        if created:
            org1_user.set_password('org123')
            org1_user.save()
            OrganizerProfile.objects.create(
                user=org1_user,
                organization_name="Global Tech Summits Inc.",
                phone="+1 415-555-0199",
                organization_description="Pioneers in organizing global technology and artificial intelligence conferences.",
                website="https://globaltechsummits.example.com"
            )

        # Organizer 2
        org2_user, created = User.objects.get_or_create(
            username='innovate_org',
            defaults={'email': 'events@innovatelabs.com', 'first_name': 'Innovate', 'last_name': 'Labs'}
        )
        if created:
            org2_user.set_password('org123')
            org2_user.save()
            OrganizerProfile.objects.create(
                user=org2_user,
                organization_name="Innovate Hackathons & Labs",
                phone="+1 212-555-0188",
                organization_description="Empowering developers through high-stakes hackathons and innovation workshops.",
                website="https://innovatelabs.example.com"
            )

        # Participant 1
        part1_user, created = User.objects.get_or_create(
            username='john_doe',
            defaults={'email': 'john.doe@example.com', 'first_name': 'John', 'last_name': 'Doe'}
        )
        if created:
            part1_user.set_password('user123')
            part1_user.save()
            ParticipantProfile.objects.create(
                user=part1_user,
                phone="+1 555-014-8821",
                bio="Full-stack software developer passionate about cloud computing and AI."
            )

        # Participant 2
        part2_user, created = User.objects.get_or_create(
            username='sarah_connor',
            defaults={'email': 'sarah.c@example.com', 'first_name': 'Sarah', 'last_name': 'Connor'}
        )
        if created:
            part2_user.set_password('user123')
            part2_user.save()
            ParticipantProfile.objects.create(
                user=part2_user,
                phone="+1 555-019-4412",
                bio="UX Designer and tech festival enthusiast."
            )

        # 3. Events with realistic images
        today = timezone.now().date()
        
        sample_events = [
            {
                'organizer': org1_user,
                'category': categories_dict['Technology'],
                'title': 'Global AI & Cloud Summit 2026',
                'description': 'Join 500+ world-class engineers, data scientists, and cloud architects to explore generative AI models, LLM deployment, and scalable cloud infrastructure. Features keynote presentations, live code demos, and networking lunches.',
                'image': 'events/tech_summit.jpg',
                'date': today + datetime.timedelta(days=15),
                'start_time': datetime.time(9, 0),
                'end_time': datetime.time(17, 30),
                'location': 'Grand Convention Center, Hall A, San Francisco, CA',
                'price': 49.99,
                'capacity': 100,
                'status': 'approved'
            },
            {
                'organizer': org2_user,
                'category': categories_dict['Hackathon'],
                'title': 'NextGen Web3 & AI Hackathon',
                'description': 'A 48-hour continuous hackathon bringing together software engineers, designers, and domain experts. Build groundbreaking decentralized AI tools and compete for $25,000 in cash prizes!',
                'image': 'events/hackathon.jpg',
                'date': today + datetime.timedelta(days=22),
                'start_time': datetime.time(10, 0),
                'end_time': datetime.time(20, 0),
                'location': 'Innovate Campus Tech Lab, New York, NY',
                'price': 0.00,
                'capacity': 60,
                'status': 'approved'
            },
            {
                'organizer': org1_user,
                'category': categories_dict['Workshop'],
                'title': 'Mastering Django & React Full-Stack Architecture',
                'description': 'An intensive hands-on masterclass focusing on high-performance REST APIs, Django ORM optimization, authentication tokens, and modern frontend integration.',
                'image': 'events/workshop.jpg',
                'date': today + datetime.timedelta(days=30),
                'start_time': datetime.time(13, 0),
                'end_time': datetime.time(16, 30),
                'location': 'Online Virtual Workshop (Zoom HD)',
                'price': 19.99,
                'capacity': 40,
                'status': 'approved'
            },
            {
                'organizer': org2_user,
                'category': categories_dict['Conference'],
                'title': 'CyberSecurity & Privacy Leaders Expo 2026',
                'description': 'Discover the latest threats in zero-trust architecture, cloud security, and quantum cryptography. Industry chief security officers share actionable insights.',
                'image': 'events/cybersecurity.jpg',
                'date': today + datetime.timedelta(days=45),
                'start_time': datetime.time(9, 30),
                'end_time': datetime.time(18, 0),
                'location': 'Metropolitan Expo Auditorium, Austin, TX',
                'price': 79.00,
                'capacity': 120,
                'status': 'approved'
            },
            {
                'organizer': org1_user,
                'category': categories_dict['Cultural & Music'],
                'title': 'Indie Beats & Code Cultural Festival',
                'description': 'An evening celebration of indie electronic music, digital artwork installations, live DJ sets, and tech community mingling.',
                'image': 'events/music_fest.jpg',
                'date': today + datetime.timedelta(days=10),
                'start_time': datetime.time(18, 0),
                'end_time': datetime.time(23, 0),
                'location': 'Sunset Amphitheater, Seattle, WA',
                'price': 15.00,
                'capacity': 200,
                'status': 'approved'
            },
            {
                'organizer': org2_user,
                'category': categories_dict['Education'],
                'title': 'Quantum Computing Fundamentals Seminar',
                'description': 'An introduction to qubit manipulation, quantum algorithms, and how quantum computers will reshape cryptography and chemistry.',
                'image': 'events/quantum.jpg',
                'date': today + datetime.timedelta(days=5),
                'start_time': datetime.time(14, 0),
                'end_time': datetime.time(17, 0),
                'location': 'University Science Center, Boston, MA',
                'price': 0.00,
                'capacity': 50,
                'status': 'approved'
            }
        ]

        created_events = []
        for evt in sample_events:
            e, created = Event.objects.get_or_create(
                title=evt['title'],
                defaults=evt
            )
            if not created and not e.image:
                e.image = evt['image']
                e.save()
            created_events.append(e)

        # 4. Registrations & Tickets
        event1 = created_events[0]
        reg1, r1_created = Registration.objects.get_or_create(
            participant=part1_user,
            event=event1,
            defaults={'status': 'registered'}
        )
        if r1_created or not hasattr(reg1, 'ticket'):
            t1 = Ticket.objects.create(
                registration=reg1,
                ticket_id=generate_unique_ticket_id()
            )
            create_ticket_qr_code(t1)
            t1.save()

        event2 = created_events[1]
        reg2, r2_created = Registration.objects.get_or_create(
            participant=part2_user,
            event=event2,
            defaults={'status': 'registered'}
        )
        if r2_created or not hasattr(reg2, 'ticket'):
            t2 = Ticket.objects.create(
                registration=reg2,
                ticket_id=generate_unique_ticket_id()
            )
            create_ticket_qr_code(t2)
            t2.save()

        self.stdout.write(self.style.SUCCESS("Successfully seeded EventHub database with sample categories, events with images, users, registrations, and QR tickets!"))

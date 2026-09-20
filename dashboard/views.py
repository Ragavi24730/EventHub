from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from events.models import Event
from registrations.models import Registration

@login_required
def participant_dashboard_view(request):
    if request.user.is_organizer_user and not Registration.objects.filter(participant=request.user).exists():
        # If user is purely an organizer and has no registrations, default suggestion
        pass

    user_registrations = Registration.objects.filter(participant=request.user).select_related('event', 'ticket').order_by('-registration_date')
    active_registrations = user_registrations.filter(status='registered')
    cancelled_registrations = user_registrations.filter(status='cancelled')

    today = timezone.now().date()
    upcoming_events_count = active_registrations.filter(event__date__gte=today).count()
    completed_events_count = active_registrations.filter(event__date__lt=today).count()
    active_tickets_count = active_registrations.count()

    context = {
        'user_registrations': user_registrations,
        'active_registrations': active_registrations,
        'cancelled_registrations': cancelled_registrations,
        'total_registered_count': active_registrations.count(),
        'upcoming_events_count': upcoming_events_count,
        'completed_events_count': completed_events_count,
        'active_tickets_count': active_tickets_count,
    }
    return render(request, 'dashboard/participant_dashboard.html', context)

@login_required
def organizer_dashboard_view(request):
    if not request.user.is_organizer_user and not request.user.is_superuser:
        messages.info(request, "Participant dashboard loaded. To host events, update your profile role to Organizer.")
        return redirect('participant_dashboard')

    events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    
    total_events = events.count()
    approved_events = events.filter(status='approved').count()
    pending_events = events.filter(status='pending').count()
    rejected_events = events.filter(status='rejected').count()

    total_registrations = sum(e.registered_count for e in events)
    total_capacity = sum(e.capacity for e in events)
    total_available_seats = sum(e.available_seats for e in events)

    context = {
        'events': events,
        'total_events': total_events,
        'approved_events': approved_events,
        'pending_events': pending_events,
        'rejected_events': rejected_events,
        'total_registrations': total_registrations,
        'total_capacity': total_capacity,
        'total_available_seats': total_available_seats,
    }
    return render(request, 'dashboard/organizer_dashboard.html', context)

@login_required
def event_participants_view(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, "You are not authorized to view participants for this event.")
        return redirect('organizer_dashboard')

    registrations = Registration.objects.filter(event=event).select_related('participant', 'ticket', 'participant__participant_profile').order_by('-registration_date')

    context = {
        'event': event,
        'registrations': registrations,
        'total_participants': registrations.filter(status='registered').count(),
    }
    return render(request, 'dashboard/event_participants.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from .models import Registration, Ticket
from .utils import generate_unique_ticket_id, create_ticket_qr_code

@login_required
def register_for_event_view(request, slug):
    event = get_object_or_404(Event, slug=slug)

    # Validate event status
    if event.status != 'approved':
        messages.error(request, "Cannot register for an event that is not approved.")
        return redirect('event_detail', slug=event.slug)

    # Validate seat availability
    if event.is_full:
        messages.error(request, "Sorry, this event is fully booked!")
        return redirect('event_detail', slug=event.slug)

    # Check for existing registration
    existing_reg = Registration.objects.filter(participant=request.user, event=event).first()

    if existing_reg:
        if existing_reg.status == 'registered':
            messages.info(request, "You are already registered for this event.")
            if hasattr(existing_reg, 'ticket'):
                return redirect('ticket_detail', ticket_id=existing_reg.ticket.ticket_id)
            return redirect('participant_dashboard')
        else:
            # Re-activate cancelled registration
            existing_reg.status = 'registered'
            existing_reg.save()
            
            # Re-issue or fetch ticket
            if not hasattr(existing_reg, 'ticket'):
                ticket_id = generate_unique_ticket_id()
                ticket = Ticket.objects.create(registration=existing_reg, ticket_id=ticket_id)
                create_ticket_qr_code(ticket)
                ticket.save()
            else:
                ticket = existing_reg.ticket
                
            messages.success(request, f"Registration re-activated! Ticket ID: {ticket.ticket_id}")
            return redirect('ticket_detail', ticket_id=ticket.ticket_id)

    # New registration
    registration = Registration.objects.create(
        participant=request.user,
        event=event,
        status='registered'
    )

    ticket_id = generate_unique_ticket_id()
    ticket = Ticket.objects.create(registration=registration, ticket_id=ticket_id)
    create_ticket_qr_code(ticket)
    ticket.save()

    messages.success(request, f"Successfully registered for {event.title}! Your digital ticket has been issued.")
    return redirect('ticket_detail', ticket_id=ticket.ticket_id)

@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)

    # Permission check: ticket owner, event organizer, or admin
    is_owner = request.user == ticket.registration.participant
    is_organizer = request.user == ticket.registration.event.organizer
    is_admin = request.user.is_superuser

    if not (is_owner or is_organizer or is_admin):
        messages.error(request, "You are not authorized to view this ticket.")
        return redirect('home')

    context = {
        'ticket': ticket,
        'registration': ticket.registration,
        'event': ticket.registration.event,
        'participant': ticket.registration.participant,
    }
    return render(request, 'registrations/ticket_detail.html', context)

@login_required
def cancel_registration_view(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, participant=request.user)

    if request.method == 'POST':
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, f"Your registration for '{registration.event.title}' has been cancelled.")
        return redirect('participant_dashboard')

    return render(request, 'registrations/registration_confirm_cancel.html', {'registration': registration})

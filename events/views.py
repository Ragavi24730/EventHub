from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Event, Category
from .forms import EventForm
from registrations.models import Registration

def home_view(request):
    categories = Category.objects.all()
    upcoming_events = Event.objects.filter(
        status='approved',
        date__gte=timezone.now().date()
    ).order_selection = ['date', 'start_time'] if hasattr(Event.objects, 'order_selection') else None
    
    approved_events = Event.objects.filter(status='approved').order_by('date', 'start_time')
    featured_events = approved_events[:6]
    
    context = {
        'categories': categories,
        'featured_events': featured_events,
        'total_events_count': approved_events.count(),
    }
    return render(request, 'home.html', context)

def event_list_view(request):
    events = Event.objects.filter(status='approved').order_by('date', 'start_time')
    categories = Category.objects.all()

    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        events = events.filter(
            Q(title__icontains=q) | 
            Q(description__icontains=q) | 
            Q(location__icontains=q)
        )

    # Category filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        events = events.filter(category=selected_category)

    # Date filter
    date_filter = request.GET.get('date', '').strip()
    if date_filter:
        events = events.filter(date=date_filter)

    # Location filter
    location_filter = request.GET.get('location', '').strip()
    if location_filter:
        events = events.filter(location__icontains=location_filter)

    context = {
        'events': events,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': q,
        'date_filter': date_filter,
        'location_filter': location_filter,
    }
    return render(request, 'events/event_list.html', context)

def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    # If event is not approved, only the organizer or superuser can view it
    if event.status != 'approved':
        if not request.user.is_authenticated or (request.user != event.organizer and not request.user.is_superuser):
            messages.error(request, "This event is currently pending approval or unavailable.")
            return redirect('event_list')

    is_registered = False
    user_registration = None
    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(
            participant=request.user, 
            event=event, 
            status='registered'
        ).first()
        if user_registration:
            is_registered = True

    context = {
        'event': event,
        'is_registered': is_registered,
        'user_registration': user_registration,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def create_event_view(request):
    if not request.user.is_organizer_user and not request.user.is_superuser:
        messages.warning(request, "Only event organizers can create new events. Please update your profile or register as an organizer.")
        return redirect('profile')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.status = 'pending' # Default status is pending admin approval
            event.save()
            messages.success(request, f"Event '{event.title}' created successfully! It is now pending admin approval.")
            return redirect('organizer_dashboard')
        else:
            messages.error(request, "Please fix the errors in the event form.")
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create New Event'})

@login_required
def edit_event_view(request, slug):
    event = get_object_or_404(Event, slug=slug)

    # Permission check: owner or superuser
    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit this event.")
        return redirect('organizer_dashboard')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('organizer_dashboard')
        else:
            messages.error(request, "Please fix errors in the event edit form.")
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {'form': form, 'event': event, 'title': 'Edit Event'})

@login_required
def delete_event_view(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.user != event.organizer and not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('organizer_dashboard')

    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f"Event '{title}' deleted successfully.")
        return redirect('organizer_dashboard')

    return render(request, 'events/event_confirm_delete.html', {'event': event})

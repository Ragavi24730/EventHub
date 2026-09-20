from django.contrib import admin
from .models import Registration, Ticket

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'status', 'registration_date')
    list_filter = ('status', 'registration_date')
    search_fields = ('participant__username', 'participant__email', 'event__title')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'get_participant', 'get_event', 'issued_at')
    search_fields = ('ticket_id', 'registration__participant__username', 'registration__event__title')

    def get_participant(self, obj):
        return obj.registration.participant.username
    get_participant.short_description = "Participant"

    def get_event(self, obj):
        return obj.registration.event.title
    get_event.short_description = "Event"

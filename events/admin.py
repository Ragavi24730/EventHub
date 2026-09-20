from django.contrib import admin
from .models import Category, Event

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_name')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'organizer', 'date', 'location', 'price', 'capacity', 'registered_count_display', 'available_seats_display', 'status', 'created_at')
    list_filter = ('status', 'category', 'date', 'created_at')
    search_fields = ('title', 'description', 'location', 'organizer__username', 'organizer__email')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_events', 'reject_events']

    def registered_count_display(self, obj):
        return obj.registered_count
    registered_count_display.short_description = "Registrations"

    def available_seats_display(self, obj):
        return obj.available_seats
    available_seats_display.short_description = "Seats Left"

    @admin.action(description="Approve selected events")
    def approve_events(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"Successfully approved {updated} event(s).")

    @admin.action(description="Reject selected events")
    def reject_events(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"Successfully rejected {updated} event(s).")

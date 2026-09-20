from django.contrib import admin
from .models import ParticipantProfile, OrganizerProfile

@admin.register(ParticipantProfile)
class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user', 'phone', 'website', 'created_at')
    search_fields = ('organization_name', 'user__username', 'user__email', 'phone')

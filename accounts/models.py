from django.db import models
from django.contrib.auth.models import User

class ParticipantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant_profile')
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/participants/', default='profiles/default.png', blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participant: {self.user.get_full_name() or self.user.username}"

class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer_profile')
    organization_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    organization_description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Organizer: {self.organization_name} ({self.user.username})"

# Dynamic property helpers for User model
@property
def is_organizer(self):
    return hasattr(self, 'organizer_profile')

@property
def is_participant(self):
    return hasattr(self, 'participant_profile')

User.add_to_class('is_organizer_user', is_organizer)
User.add_to_class('is_participant_user', is_participant)

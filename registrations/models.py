from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class Registration(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
    )

    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')

    class Meta:
        unique_together = ('participant', 'event')
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.participant.username} - {self.event.title} ({self.status})"

class Ticket(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='ticket')
    ticket_id = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} for {self.registration.participant.username}"

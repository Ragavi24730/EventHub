from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default='calendar', help_text="FontAwesome icon class name e.g. laptop-code, music, trophy")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', default='events/default.jpg', blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    capacity = models.PositiveIntegerField(default=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Event.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def registered_count(self):
        return self.registrations.filter(status='registered').count()

    @property
    def available_seats(self):
        return max(0, self.capacity - self.registered_count)

    @property
    def is_full(self):
        return self.available_seats <= 0

    @property
    def is_free(self):
        return self.price == 0 or self.price == 0.00

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

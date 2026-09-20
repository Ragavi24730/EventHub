from django.urls import path
from . import views

urlpatterns = [
    path('events/<slug:slug>/register/', views.register_for_event_view, name='register_event'),
    path('ticket/<str:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('registration/<int:registration_id>/cancel/', views.cancel_registration_view, name='cancel_registration'),
]

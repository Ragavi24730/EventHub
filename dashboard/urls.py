from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/participant/', views.participant_dashboard_view, name='participant_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard_view, name='organizer_dashboard'),
    path('dashboard/organizer/events/<slug:slug>/participants/', views.event_participants_view, name='event_participants'),
]

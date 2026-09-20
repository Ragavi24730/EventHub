from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('events/', views.event_list_view, name='event_list'),
    path('events/create/', views.create_event_view, name='create_event'),
    path('events/<slug:slug>/', views.event_detail_view, name='event_detail'),
    path('events/<slug:slug>/edit/', views.edit_event_view, name='edit_event'),
    path('events/<slug:slug>/delete/', views.delete_event_view, name='delete_event'),
]

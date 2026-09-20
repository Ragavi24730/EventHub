from django import forms
from .models import Event, Category

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}))

    class Meta:
        model = Event
        fields = ['title', 'category', 'description', 'image', 'date', 'start_time', 'end_time', 'location', 'price', 'capacity']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. AI & Tech Summit 2026', 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Detailed event overview, agenda, speakers...', 'class': 'form-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Grand Convention Center, San Francisco or Online (Zoom)', 'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.00 for free events', 'class': 'form-input'}),
            'capacity': forms.NumberInput(attrs={'min': '1', 'placeholder': 'Maximum attendee capacity', 'class': 'form-input'}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity < 1:
            raise forms.ValidationError("Capacity must be at least 1 seat.")
        return capacity

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

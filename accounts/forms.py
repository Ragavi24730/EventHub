from django import forms
from django.contrib.auth.models import User
from .models import ParticipantProfile, OrganizerProfile

class UserRegisterForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('participant', 'Participant (Attend & Register for Events)'),
        ('organizer', 'Organizer (Create & Host Events)'),
    )
    
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose password'}), min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='participant')
    
    # Organizer specific optional initial field
    organization_name = forms.CharField(max_length=150, required=False, help_text="Required if registering as an organizer")
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')
        org_name = cleaned_data.get('organization_name')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if role == 'organizer' and not org_name:
            self.add_error('organization_name', "Organization name is required for organizers.")

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ParticipantProfileForm(forms.ModelForm):
    class Meta:
        model = ParticipantProfile
        fields = ['phone', 'bio', 'profile_image']

class OrganizerProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizerProfile
        fields = ['organization_name', 'phone', 'organization_description', 'website']

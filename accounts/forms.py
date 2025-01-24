


from django import forms
from travello.models import Guide, Availability, Booking
from django.contrib.auth.hashers import make_password


class GuideForm(forms.ModelForm):
    class Meta:
      model = Guide
      fields = ['civility', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'city_or_region', 'mother_tongue', 'tour_languages', 'presentation', 'photo', 'certified_guide', 'guide_card', 'message', 'price','username', 'password']
      widgets = {
         'password': forms.PasswordInput(),
      }
    def save(self, commit=True):
     guide = super().save(commit=False)
     guide.password = make_password(self.cleaned_data['password']) #hash the password
     if commit:
        guide.save()
     return guide

class ReplyForm(forms.Form):
   reply = forms.CharField(widget=forms.Textarea)

class BookingForm(forms.ModelForm):
    class Meta:
        accept_terms = forms.BooleanField(required=True)
        model = Booking
        fields = [
            'first_name',
            'last_name',
            'email',
            'preferred_date',
            'party_size',
            'message',
            'accept_terms',
            'accept_marketing_emails'
   
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email address'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'party_size': forms.NumberInput(attrs={'class': 'party-size'}),
            'message': forms.Textarea(attrs={'placeholder': 'Type your message here'}),
        }


from django.forms.widgets import DateTimeInput

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': DateTimeInput(attrs={'type':'datetime-local'}),
            'end_date': DateTimeInput(attrs={'type':'datetime-local'}),
        }
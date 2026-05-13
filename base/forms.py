from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'room_name', 'placeholder': 'E.g. Mastering Python + Django'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write about your study group...'}),
        }

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'username',
                'placeholder': 'e.g. mustafo',
            })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'id': 'password', 'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'id': 'confirm_password', 'placeholder': '••••••••'})

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("avatar", "first_name", "last_name", "username", "email", "bio")

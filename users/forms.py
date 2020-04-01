from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'description', 'pic')
        labels = {
            'description': _('Bio'),
            
        }
        widgets = {
                'description': forms.Textarea(attrs={'rows':4}),
            }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'description', 'pic')
        labels = {
            'description': _('Bio'),
            
        }
        widgets = {
                'description': forms.Textarea(attrs={'rows':4}),
            }
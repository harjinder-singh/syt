from django import forms
from comments.models import *
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': _('Comment:'),
        }

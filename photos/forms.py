from PIL import Image
from django import forms
from django.core.files import File
from .models import Photo

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('pic', 'description','user', 'x', 'y', 'width', 'height', )
    
    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        hide_condition = kwargs.pop('hide_condition',None)
        super(PhotoForm, self).__init__(*args, **kwargs)
        if hide_condition:
            self.fields['user'].widget = HiddenInput()

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.pic)
        cropped_image = image.crop((x, y, w+x, h+y))
        cropped_image.save(photo.pic.path,"JPEG", quality=100)

        return photo

class EditPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('description','user')

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        hide_condition = kwargs.pop('hide_condition',None)
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        if hide_condition:
            self.fields['user'].widget = HiddenInput() 
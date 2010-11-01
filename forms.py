from django import forms
from models import Upload

class UploadFileForm(forms.ModelForm):
    # name gets derived automaticaly from os path
    #name = forms.CharField(max_length=50)
    file  = forms.FileField()
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Upload
        fields = ('file', 'description')

    def save(self, request, obj, *args, **kwargs):
        self.instance.set_file(self.cleaned_data['file'])
        super(UploadFileForm, self).save(*args, **kwargs)


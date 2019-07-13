from django import forms


class UploadFileForm(forms.Form):
    data_file = forms.FileField()

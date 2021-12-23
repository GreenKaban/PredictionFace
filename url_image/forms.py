from django import forms


class UrlsForm(forms.Form):
    photo_first_url = forms.ImageField(label='First photo')
    photo_second_url = forms.ImageField(label='Second photo')
    email = forms.EmailField(label='Email for report', required=False)

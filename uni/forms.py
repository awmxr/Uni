from django import forms

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput)

class Loginform2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


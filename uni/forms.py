from django import forms

class Loginform(forms.Form):
    username = forms.CharField()
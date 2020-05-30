from django import forms

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput, label = False)

class Loginform2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label = False)

class sabtform(forms.Form):
    sabt = forms.CharField(widget = forms.TextInput , label = False)


    


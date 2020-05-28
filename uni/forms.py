from django import forms

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput)

class Loginform2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

list1 = [('Student','Student'),
            ('Admin','admin')]
# class Choice(forms.Form):
#     choos = forms.MultipleChoiceField(
#         required=False,
#         widget=forms.RadioSelect,
#         choices=list1
        
    # )
from django import forms
from .models import Student

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = False)


class Loginform2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label = False)

class sabtform(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'username',
            'name',
            'last_name',
            'father_name',
            'melli_code',
            'enter_year',
            'uni',
            'College',
            'password',
            'phone',
            'field',
            'student_live',
            'parents_phone',
        ]
        widgets = {
            'password' : forms.PasswordInput
        } 
        labels = {
            "username": "شماره دانشجویی",
            'name':'نام',
            'father_name':'نام پدر',
            'melli_code':'کد ملی',
            'enter_year': ' ورودی',
            'uni':'دانشگاه',
            'College':'دانشکده',
            'last_name':'نام خانوادگی',
            'password':'پسوورد',
            'phone':'تلفن همراه دانشجو',
            'field':'رشته تحصیلی',
            'student_live':'محل سکونت',
            'parents_phone':'تلفن همراه والد',
            
        }


    


from django import forms
from .models import Student
from . import choices

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = False)


class Loginform2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label = False)

class sabtform(forms.ModelForm):
    # field = forms.CharField(widget = forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False 
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
            'field',
            'password',
            'phone',
            'student_live',
            'religion',
            'parents_phone',
        ]
        widgets = {
            'password' : forms.PasswordInput,
            'student_live': forms.Select(choices= choices.live_choices),
            'uni': forms.Select(choices= choices.uni_choices),
            'College': forms.Select(choices= choices.college_choices,attrs={'onchange': 'submit();'}),
            'religion' : forms.Select(choices= choices.religion_choices),
            'enter_year': forms.Select(choices= choices.enter_year_choices),
            # 'field': forms.HiddenInput(),
            'field': forms.Select(),
            
        } 
        
        
        labels = {
            'religion':'مذهب',
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
        


    


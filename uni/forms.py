from django import forms
from .models import Student,Exter,Ostad
from . import choices

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = False)


class Loginform2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label = False)

class sabtform(forms.ModelForm):
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
            'grade',
            'course',
            'College',
            'field',
            'password',
            'phone',
            'student_live',
            'religion',
            'parents_phone',
            
            # 'birthday'
        ]
        widgets = {
            'password' : forms.PasswordInput,
            'student_live': forms.Select(choices= choices.live_choices),
            'uni': forms.Select(choices= choices.uni_choices),
            'College': forms.Select(choices= choices.college_choices,attrs={'onchange': 'submit();'}),
            'religion' : forms.Select(choices= choices.religion_choices),
            'enter_year': forms.Select(choices= choices.enter_year_choices),
            'grade': forms.Select(choices= choices.grade_choices),
            'course': forms.Select(choices= choices.course_choices),
            'field': forms.Select(),
            # 'username':forms.TextInput(attrs = {'placeholder':'شماره دانشجویی'}),
            # 'name' : forms.TextInput(attrs = {'placeholder':'نام'}),
            
            
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
            'birthday':'تاریخ تولد',
            'grade':'مقطع تحصیلی',
            'course':'دوره آموزشی',
            
        }


class ChangeForm(forms.ModelForm):
    class Meta:
        model = Student

        fields = [
            'username',
            'name',
            'last_name',
            'father_name',
            'melli_code',
            'phone',
            'student_live',
            'religion',
            'parents_phone',
        ]
        labels = {
            'religion':'مذهب',
            "username": "شماره دانشجویی",
            'name':'نام',
            'father_name':'نام پدر',
            'melli_code': 'کد ملی',
            'last_name':'نام خانوادگی',
            'phone':'تلفن همراه دانشجو',
            'student_live':'محل سکونت',
            'parents_phone':'تلفن همراه والد',
            
        }
class ChangePass(forms.Form):
    pass1 = forms.CharField(widget = forms.PasswordInput,label = 'پسوورد قدیمی')
    pass2 = forms.CharField(widget = forms.PasswordInput,label = 'پسوورد جدید')
    pass3 = forms.CharField(widget = forms.PasswordInput,label = ' تکرار پسوورد جدید')

class ChangePass2(forms.Form):
    pass2 = forms.CharField(widget = forms.PasswordInput,label = 'پسوورد جدید')
    pass3 = forms.CharField(widget = forms.PasswordInput,label = ' تکرار پسوورد جدید')

class Change2Form(forms.ModelForm):
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
            'grade',
            'course',
            'College',
            'field',
            'phone',
            'student_live',
            'religion',
            'parents_phone',
            
            'birthday'
        ]
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
            'birthday':'تاریخ تولد',
            'grade':'مقطع تحصیلی',
            'course':'دوره آموزشی',
            
        }
        widgets = {
            'password' : forms.PasswordInput,
            'student_live': forms.Select(choices= choices.live_choices),
            'uni': forms.Select(choices= choices.uni_choices),
            # 'College': forms.Select(choices= choices.college_choices,attrs={'onchange': 'submit();'}),
            'religion' : forms.Select(choices= choices.religion_choices),
            'enter_year': forms.Select(choices= choices.enter_year_choices),
            'grade': forms.Select(choices= choices.grade_choices),
            'course': forms.Select(choices= choices.course_choices),
            # 'field': forms.Select(),
            # 'username':forms.TextInput(attrs = {'placeholder':'شماره دانشجویی'}),
            # 'name' : forms.TextInput(attrs = {'placeholder':'نام'}),
            
            
        } 

class ElamForm(forms.ModelForm):
    class Meta:
        fields = [
            'term',
            'college',
            'fields',
            'dars',
            'numbers',
            'capacity',
            'time',
        ]





class sabtform2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False 
    class Meta:
        
        model = Ostad
        fields = [
            'username',
            'name',
            'last_name',
            
            'melli_code',
            'uni',
            'grade',
            'field',
            'password',
            'phone',
            'religion',
            
        ]
        widgets = {
            'password' : forms.PasswordInput,
            
            'uni': forms.Select(choices= choices.uni_choices),
            
            'religion' : forms.Select(choices= choices.religion_choices),
            
            'grade': forms.Select(choices= choices.grade_choices),
            
            'field': forms.Select(choices= choices.field1_choices + choices.field2_choices + choices.fileld3_choices + choices.fileld4_choices + choices.fileld5_choices),
            
            
            
        } 
        
        
        labels = {
            'religion':'مذهب',
            "username": "شماره دانشجویی",
            'name':'نام',
            
            'melli_code':'کد ملی',
            'uni':'دانشگاه',
            'last_name':'نام خانوادگی',
            'password':'پسوورد',
            'phone':'تلفن همراه دانشجو',
            'field':'رشته تحصیلی',
            'grade':'مقطع تحصیلی',
        }


        





        


    


from django import forms

from .models import Student,Ostad,Elam,Klass,Boss,Admin2



from . import choices
from django.contrib.auth import authenticate

class Loginform(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = False)
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
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'father_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'melli_code': forms.TextInput(attrs={'autocomplete': 'off'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'off'}),
            'parents_phone': forms.TextInput(attrs={'autocomplete': 'off'}),
            
            'student_live': forms.Select(choices= choices.live_choices),
            'uni': forms.Select(choices= choices.uni_choices),
            'College': forms.Select(choices= choices.college_choices),
            'religion' : forms.Select(choices= choices.religion_choices),
            'enter_year': forms.Select(choices= choices.enter_year_choices),
            'grade': forms.Select(choices= choices.grade_choices),
            'course': forms.Select(choices= choices.course_choices),
            'field': forms.Select(choices = choices.field1_choices + choices.field2_choices + choices.fileld3_choices + choices.fileld4_choices+choices.fileld5_choices),
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
            
            'name',
            'last_name',
            
        
            'phone',
            'student_live',
            'religion',
            
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
        widgets = {
            'student_live': forms.Select(choices= choices.live_choices),            
            'religion' : forms.Select(choices= choices.religion_choices),
            
 
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
            'College': forms.Select(choices= choices.college_choices),
            'religion' : forms.Select(choices= choices.religion_choices),
            'enter_year': forms.Select(choices= choices.enter_year_choices),
            'grade': forms.Select(choices= choices.grade_choices),
            'course': forms.Select(choices= choices.course_choices),
            'field': forms.Select(choices = choices.field1_choices +choices.field2_choices + choices.fileld3_choices + choices.fileld4_choices+choices.fileld5_choices),
            # 'username':forms.TextInput(attrs = {'placeholder':'شماره دانشجویی'}),
            # 'name' : forms.TextInput(attrs = {'placeholder':'نام'}),
            
            
        } 








# 


        


class ElamForm(forms.ModelForm):

    class Meta:
        model = Elam
        fields = [
            'username',
            'ostad',
            'uni',
            'college',
            'dars',
            'sex',
            'capacity',
            'phone',
            
            
            
          
        ]
        labels = {
            'college' : 'دانشکده',
            'dars' : 'درس',
            'capacity' : 'ظرفیت',
            'uni':'دانشگاه',
            'sex':'جنسیت'

        }
        

        widgets = {
            'college' : forms.Select(choices= choices.college_choices),
            'dars' : forms.Select(choices= choices.dars_choices),  
            'sex' : forms.Select(choices= choices.sex_choices), 
            'username' : forms.HiddenInput(),
            'ostad':forms.HiddenInput(),
            'phone' : forms.HiddenInput(),
            # 'ostad_id' : forms.HiddenInput(),
            'uni':forms.Select(choices= choices.uni_choices),
            
            
        } 
        





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
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'melli_code': forms.TextInput(attrs={'autocomplete': 'off'}),
            
            'phone': forms.TextInput(attrs={'autocomplete': 'off'}),
            
            'password' : forms.PasswordInput,
            
            'uni': forms.Select(choices= choices.uni_choices),
            
            'religion' : forms.Select(choices= choices.religion_choices),
            
            'grade': forms.Select(choices= choices.grade_choices),
            
            'field': forms.Select(choices= choices.field1_choices + choices.field2_choices + choices.fileld3_choices + choices.fileld4_choices + choices.fileld5_choices),
            
            
            
        } 
        
        
        labels = {
            'religion':'مذهب',
            "username": "کد کاربری",
            'name':'نام',
            'melli_code':'کد ملی',
            'uni':'دانشگاه',
            'last_name':'نام خانوادگی',
            'password':'پسوورد',
            'phone':'تلفن همراه استاد',
            'field':'رشته تحصیلی',
            'grade':'مقطع تحصیلی',
        }





class sabtform3(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False 
    class Meta:
        
        model = Boss
        fields = [
            'username',
            'name',
            'last_name',
            'uni',
            'password',
            'phone',
            
            
        ]
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'off'}),
            'password' : forms.PasswordInput,
            
            'uni': forms.Select(choices= choices.uni_choices),
            
            
            
        } 
        
        
        labels = {
            
            "username": "شماره کاربری",
            'name':'نام',
            
            'uni':'دانشگاه',
            'last_name':'نام خانوادگی',
            'password':'پسوورد',
            'phone':'تلفن همراه',
        }









class sabtform4(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False 
    class Meta:
        
        model = Admin2
        fields = [
            'username',
            'name',
            'last_name',
            'College',
            'password',
            'phone',
            
            
        ]
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'off'}),
            'password' : forms.PasswordInput,
            'college': forms.Select(choices= choices.college_choices),
            
            
            
        } 
        
        
        labels = {
            
            "username": "شماره کاربری",
            'name':'نام',
            'College':'دانشکده',
            'uni':'دانشگاه',
            'last_name':'نام خانوادگی',
            'password':'پسوورد',
            'phone':'تلفن همراه',
        }





class KlassForm(forms.ModelForm):
    class Meta:
        model = Klass
        fields = [
            'number',
            'college',
            'floor',
            'public_date',
            'uni',
            'khali',
        ]
        widgets = {
            'number': forms.TextInput(attrs={'autocomplete': 'off'}),
            'floor': forms.TextInput(attrs={'autocomplete': 'off'}),
            
            'college' : forms.HiddenInput(),
            'address' : forms.Textarea() ,  
            'public_date' : forms.HiddenInput(),
            'uni':forms.HiddenInput(),
            'khali':forms.HiddenInput(),
        }
        labels = {
            'number':'شماره کلاس',
            'floor':'طبقه'
        }
class EntekhabForm(forms.Form):
    goruh = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = 'گروه درس')
    codedars = forms.CharField(widget=forms.TextInput,label = 'کد درس')

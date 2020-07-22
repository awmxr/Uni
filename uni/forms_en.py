from django import forms

from .models import Student,Ostad,Elam,Klass,Boss,Admin2



from . import choices_en
from django.contrib.auth import authenticate

class Loginform_en(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = 'Username')
    password = forms.CharField(widget=forms.PasswordInput,label = 'Password')

class sabtform_en(forms.ModelForm):
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
            
            'student_live': forms.Select(choices= choices_en.live_choices),
            'uni': forms.Select(choices= choices_en.uni_choices),
            'College': forms.Select(choices= choices_en.college_choices),
            'religion' : forms.Select(choices= choices_en.religion_choices),
            'enter_year': forms.Select(choices= choices_en.enter_year_choices),
            'grade': forms.Select(choices= choices_en.grade_choices),
            'course': forms.Select(choices= choices_en.course_choices),
            'field': forms.Select(choices = choices_en.field1_choices + choices_en.field2_choices + choices_en.fileld3_choices + choices_en.fileld4_choices+choices_en.fileld5_choices),
            # 'username':forms.TextInput(attrs = {'placeholder':'شماره دانشجویی'}),
            # 'name' : forms.TextInput(attrs = {'placeholder':'نام'}),
            
            
        } 
        
        
        labels = {
            'religion':'Religion',
            "username": "Student ID",
            'name':'First Name',
            "father_name":"Father's Name" ,
            'melli_code':'National ID',
            'enter_year': 'Entering Year',
            'uni':'University',
            'College':'College',
            'last_name':'Last Name',
            'password':'Password',
            'phone':'Phone Number',
            'field':'Field of Study',
            'student_live':'Place of Living',
            "parents_phone":"Father or Mother's Phone Number",
            'birthday':'Date of Birth',
            'grade':'Grade',
            'course':'Course',
            
        }


class ChangeForm_en(forms.ModelForm):
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
            'religion':'Religion',
            "username": "Student ID",
            'name':'First Name',
            'father_name':"Father's Name",
            'melli_code': 'National ID',
            'last_name':'Last Name',
            'phone':'Phone Number',
            'student_live':'Place of Living',
            "parents_phone":"Father or Mother's Phone Number",
            
        }
        widgets = {
            'student_live': forms.Select(choices= choices_en.live_choices),            
            'religion' : forms.Select(choices= choices_en.religion_choices),
            
 
        } 
class ChangePass_en(forms.Form):
    pass1 = forms.CharField(widget = forms.PasswordInput,label = 'Old Password')
    pass2 = forms.CharField(widget = forms.PasswordInput,label = 'New Password')
    pass3 = forms.CharField(widget = forms.PasswordInput,label = 'New Password (Again)')

class ChangePass2_en(forms.Form):
    pass2 = forms.CharField(widget = forms.PasswordInput,label = 'New Password')
    pass3 = forms.CharField(widget = forms.PasswordInput,label = 'New Password (Again)')

class Change2Form_en(forms.ModelForm):
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
            'religion':'Religion',
            "username": "Student ID",
            'name':'First Name',
            'father_name':"Father's Name",
            'melli_code':'National ID',
            'enter_year': 'Entering Year',
            'uni':'University',
            'College':'College',
            'last_name':'Last Name',
            'password':'Password',
            'phone':'Phone Number',
            'field':'Field of Study',
            'student_live':'Place of Living',
            "parents_phone":"Father or Mother's Phone Number",
            'birthday':'Date of Birth',
            'grade':'Grade',
            'course':'Course',
            
        }
        widgets = {
            'password' : forms.PasswordInput,
            'student_live': forms.Select(choices= choices_en.live_choices),
            'uni': forms.Select(choices= choices_en.uni_choices),
            'College': forms.Select(choices= choices_en.college_choices),
            'religion' : forms.Select(choices= choices_en.religion_choices),
            'enter_year': forms.Select(choices= choices_en.enter_year_choices),
            'grade': forms.Select(choices= choices_en.grade_choices),
            'course': forms.Select(choices= choices_en.course_choices),
            'field': forms.Select(choices = choices_en.field1_choices +choices_en.field2_choices + choices_en.fileld3_choices + choices_en.fileld4_choices+choices_en.fileld5_choices),
            # 'username':forms.TextInput(attrs = {'placeholder':'شماره دانشجویی'}),
            # 'name' : forms.TextInput(attrs = {'placeholder':'نام'}),
            
            
        } 














        


class ElamForm_en(forms.ModelForm):

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
            'college' : 'College',
            'dars' : 'Course',
            'capacity' : 'Capacity',
            'uni':'University',
            'sex':'Gender'

        }
        

        widgets = {
            'college' : forms.Select(choices= choices_en.college_choices),
            'dars' : forms.Select(choices= choices_en.dars_choices),  
            'sex' : forms.Select(choices= choices_en.sex_choices), 
            'username' : forms.HiddenInput(),
            'ostad':forms.HiddenInput(),
            'phone' : forms.HiddenInput(),
            # 'ostad_id' : forms.HiddenInput(),
            'uni':forms.Select(choices= choices_en.uni_choices),
            
            
        } 
        





class sabtform2_en(forms.ModelForm):
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
            
            'uni': forms.Select(choices= choices_en.uni_choices),
            
            'religion' : forms.Select(choices= choices_en.religion_choices),
            
            'grade': forms.Select(choices= choices_en.grade_choices),
            
            'field': forms.Select(choices= choices_en.field1_choices + choices_en.field2_choices + choices_en.fileld3_choices + choices_en.fileld4_choices + choices_en.fileld5_choices),
            
            
            
        } 
        
        
        labels = {
            'religion':'Religion',
            "username": "Professor ID",
            'name':'First Name',
            'melli_code':'National ID',
            'uni':'University',
            'last_name':'Last Name',
            'password':'Password',
            'phone':'Phone Number',
            'field':'Field',
            'grade':'Grade',
        }





class sabtform3_en(forms.ModelForm):
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
            
            'uni': forms.Select(choices= choices_en.uni_choices),
            
            
            
        } 
        
        
        labels = {
            
            "username": "Username",
            'name':'First Name',
            
            'uni':'University',
            'last_name':'Last Name',
            'password':'Password',
            'phone':'Phone Number',
        }









class sabtform4_en(forms.ModelForm):
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
            'college': forms.Select(choices= choices_en.college_choices),
            
            
            
        } 
        
        
        labels = {
            
            "username": "Username",
            'name':'First Name',
            
            'uni':'University',
            'last_name':'Last Name',
            'password':'Password',
            'phone':'Phone Number',
        }





class KlassForm_en(forms.ModelForm):
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
            'number':'Class ID',
            'floor':'Floor'
        }
class EntekhabForm_en(forms.Form):
    goruh = forms.CharField(widget = forms.TextInput(attrs={'autocomplete': 'off'}), label = 'Course Group')
    codedars = forms.CharField(widget=forms.TextInput,label = 'Course Code')

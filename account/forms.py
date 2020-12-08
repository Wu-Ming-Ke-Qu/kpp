from django import forms

from school.models import School
class UserForm(forms.Form):
    username = forms.CharField(label="用户名",
                               max_length=128, 
                               widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="密码", 
                               max_length=256, 
                               widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    is_rem = forms.BooleanField(required=False)

class RegisterForm(forms.Form):
    school_set = []
    try:
        for school in School.objects.all():
            school_set.append((school.id, school.school_name))
    except Exception:
        pass
    username = forms.CharField(label="用户名", 
                               max_length=128, 
                               widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="密码", 
                               max_length=256,
                               widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password_confirm = forms.CharField(label="确认密码", 
                                       max_length=256, 
                                       widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    school = forms.ChoiceField(label="学校", choices=school_set,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", 
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = forms.CharField(label="验证码",
                              max_length=6,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
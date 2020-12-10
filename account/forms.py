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
    username = forms.CharField(label="用户名", 
                               max_length=128, 
                               widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="密码", 
                               max_length=256,
                               widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password_confirm = forms.CharField(label="确认密码", 
                                       max_length=256, 
                                       widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="学校", 
                                    empty_label="请选择你的学校",
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", 
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
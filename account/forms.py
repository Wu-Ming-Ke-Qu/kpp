from django import forms

from school.models import School
class UserForm(forms.Form):
    username = forms.CharField(label="用户名",
                               max_length=128, 
                               widget=forms.TextInput(attrs={"class": 'form-control', 'style': 'border-radius: 5px;'}))
    password = forms.CharField(label="密码", 
                               max_length=256, 
                               widget=forms.PasswordInput(attrs={"class": 'form-control', 'style': 'border-radius: 5px;'}))
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

class ChangePWForm(forms.Form):
    old_password = forms.CharField(label="旧密码",
                                   max_length=256,
                                   widget=forms.PasswordInput(attrs={'class':'form-control'}))

    new_password = forms.CharField(label="新密码",
                                   max_length=256,
                                   widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    confirm_password = forms.CharField(label="确认新密码",
                                       max_length=256,
                                       widget=forms.PasswordInput(attrs={'class':'form-control'}))
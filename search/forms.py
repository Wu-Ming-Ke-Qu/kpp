from django import forms

from school.models import School

class SearchForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="学校", empty_label="请选择你的学校",
                                            widget=forms.Select(attrs={'class':'form-control', 
                                            'style':'height: 50px;width: 30%; margin-left: 0px;'}))
    course = forms.CharField(max_length=128, label="课程名", empty_value="课程名", required=False,
                             widget=forms.TextInput(attrs={'class':'form-control',
                             'style':'height: 50px;width: 70%; margin-right: 0px;'}))

class SmallSearchForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="学校", empty_label="学校",
                                            widget=forms.Select(attrs={'class':'form-control', 
                                            'style':'width:40%; font-size: x-small;'}))
    course = forms.CharField(max_length=128, label="课程名", empty_value="课程名", required=False,
                             widget=forms.TextInput(attrs={'class':'form-control', 
                             'style':'width: 60%; font-size: x-small;'}))
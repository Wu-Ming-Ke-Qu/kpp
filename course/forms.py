from django import forms

from school.models import School

class CourseForm(forms.Form):
    course_name = forms.CharField(label="课程名",
                                  max_length=128,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    course_id = forms.CharField(label="课程号",
                                max_length=128,
                                required=False,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    school = forms.ModelChoiceField(queryset=School.objects.all(),
                                    label="学校",
                                    widget=forms.Select(attrs={'class':'form-control'}))
    department = forms.CharField(label="院系",
                                 max_length=128,
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    teacher = forms.CharField(label="开课教师", 
                              max_length=128,
                              widget=forms.TextInput(attrs={'class':'form-control'}))
    credit = forms.CharField(
        label="学分", 
        max_length=128,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    hour = forms.CharField(
        label="学时", 
        max_length=128,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    pre_course = forms.CharField(label="先修要求",
                                 required=False,
                                 widget=forms.Textarea(attrs={'class':'form-control'}))

class ChangeCourseForm(forms.Form):
    credit = forms.CharField(
        label="学分",
        max_length=128,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    hour = forms.CharField(
        label="学时", 
        max_length=128,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    pre_course = forms.CharField(
        label="先修要求",
        required=False,
        widget=forms.Textarea(attrs={'class':'form-control'})
    )
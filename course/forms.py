from django import forms

from course.models import Course, CourseTeacher
from school.models import Teacher, School, Department

class CourseForm(forms.Form):
    course_name = forms.CharField(label="课程名",
                                  max_length=128,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    course_id = forms.CharField(label="课程号",
                                max_length=128,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    school = forms.ModelChoiceField(queryset=School.objects.all(),
                                    widget=forms.Select(attrs={'class':'form-control'}))
    department = forms.CharField(label="院系",
                                 max_length=128,
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    teacher = forms.CharField(label="开课教师", 
                              max_length=128,
                              widget=forms.TextInput(attrs={'class':'form-control'}))
    credit = forms.IntegerField(label="学分", 
                                widget=forms.NumberInput(attrs={'class':'form-control'}))
    hour = forms.IntegerField(label="学时", 
                              widget=forms.NumberInput(attrs={'class':'form-control'}))
    pre_course = forms.CharField(label="先修要求",
                                 widget=forms.Textarea(attrs={'class':'form-control'}))
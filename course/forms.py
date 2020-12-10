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
    school = forms.ModelField(label="课程号",
                                max_length=128,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    
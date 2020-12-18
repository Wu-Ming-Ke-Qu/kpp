from django import forms

class AddSchoolFrom(forms.Form):
    SCHOOL_TYPE_CHOICE = (
        ('大学', '大学'),
        ('中学', '中学'),
        ('小学', '小学'),
        ('特殊教育学校', '特殊教育学校'),
        ('其他', '其他'),
    )
    school_type = forms.ChoiceField(label="学校类型", choices=SCHOOL_TYPE_CHOICE, 
                                    widget=forms.Select(attrs={'class':'form-control'}))
    school_name = forms.CharField(label="学校名称", 
                                  max_length=128,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    school_email_addr = forms.CharField(label="学校邮箱后缀",
                                        max_length=128,
                                        required=False,
                                        widget=forms.TextInput(attrs={'class':'form-control'}))
from app01.models import Department,UserInfo,PrettyNum
from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

class UserModelForm(BootStrapModelForm):
    class Meta:
        model=UserInfo
        fields=["name","password","age","account","create_time","gender","depart"]

class PrettyModelForm(BootStrapModelForm):
    mobile=forms.CharField(
        label='号码',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','靓号格式错误 ')]
    )
    class Meta:
        model=PrettyNum
        fields=["mobile","price","level","status"]

    def clean_mobile(self):
        txt_mobile=self.cleaned_data['mobile']
        exists=PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('号码已存在')
        return txt_mobile
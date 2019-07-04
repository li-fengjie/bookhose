from django.contrib.auth import get_user_model
from django.core import validators
from django import forms
from django.middleware import cache

from apps.cms.models import User
from apps.froms import FormMixin


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3456789]\d{9}')])
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=30, min_length=6, error_messages={"max_length": '最多30', "min_length": '最少6'})
    password2 = forms.CharField(max_length=30, min_length=6, error_messages={"max_length": '最多30', "min_length": '最少6'})

    def clean(self):
        clean_data = super(RegisterForm, self).clean()
        telephone = clean_data.get('telephone')
        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')
        if password1 != password2:
            forms.ValidationError('两次密码输入不一致')

        # img_captcha=clean_data.get('img_captcha')
        # cached_img_captcha=cache.get(img_captcha.lower())
        # if not cached_img_captcha or cached_img_captcha.lower()!=img_captcha.lower():
        #     raise forms.ValidationError('图形验证码错误')


        # sms_captcha = clean_data.get('sms_captcha')
        # cached_sms_captcha = cache.get(sms_captcha.lower())
        # if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
        #     raise forms.ValidationError('短信验证码错误')


        telephone = clean_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        print(exists)
        if exists:
            return forms.ValidationError('该手机号已经注册')
        return clean_data


class MyLoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3456789]\d{9}')])
    password = forms.CharField(max_length=30, min_length=6, error_messages={"max_length": '最多30', "min_length": '最少6'})

    class Meta:
        model = get_user_model()
        fields = ['telephone', 'password']


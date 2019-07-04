from django import forms

from apps.cms.models import Book


class MyForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        error_messages = {
            'cover': {
                'invalid_extension': '请上传正确格式的文件'
            }
        }

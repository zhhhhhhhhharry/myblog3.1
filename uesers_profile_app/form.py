from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):#继承modelform对用户密码直接验证
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')  # 启用username和email

    # 对密码长度进行验证
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise ValidationError("密码长度必须大于或等于 6 个字符。")

        return password

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("两次输入的密码不一致，请重新输入。")

        return password2

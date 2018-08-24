from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


# 定制登录表单
class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        required=True,  # 默认为True
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名'
        }))
    # 设置渲染后的html的属性

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        }))

    # 验证数据方法
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        required=True,  # 默认为True
        max_length=30,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入3-30位用户名'
        }))
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱'
        }))

    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        }))
    password_again = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '再输入一次密码'
        }))

    # 验证数据, 是否有效，是否存在
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again
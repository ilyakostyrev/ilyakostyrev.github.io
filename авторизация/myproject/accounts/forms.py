from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile  # Импортируем модель

class RegisterForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой')
    ]
    
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'autofocus': 'true'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    password1 = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
    )
    
    # Добавляем поле для выбора пола
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Пол'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Создаем или обновляем профиль пользователя с выбранным полом
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'gender': self.cleaned_data['gender']}
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'autofocus': 'true'
        })
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']
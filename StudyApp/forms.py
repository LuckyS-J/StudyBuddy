from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Goal, Task, Note


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
        'id': 'floatingEmail'
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'id': 'floatingUsername'
            }),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'floatingUsername'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'floatingPassword'
    }))


class AddGoalForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}),
    )

    labels = {
        'title': 'Goal title',
    }

    class Meta:
        model = Goal
        fields = [
            'title',
            'description',
            'status',
            'deadline',
            'bg_photo',
        ]


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}),
        }


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'text',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ' '}),
        }

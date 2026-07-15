from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        def clean_email(self):

            email = self.cleaned_data["email"]

            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "این ایمیل قبلاً ثبت شده است."
                )

            return email
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام کاربری",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل",
            }),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "رمز عبور",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "تکرار رمز عبور",
                }
            ),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            "avatar",
            "phone",
            "bio",
        ]

        widgets = {
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "شماره تماس",
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "درباره خودتان...",
            }),
        }


class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور فعلی",
            }
        )
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور جدید",
            }
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز عبور جدید",
            }
        )
    )
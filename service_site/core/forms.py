from django import forms
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import (
    Order,
    Contact,
    JobApplication,
    Ticket,
    ProjectProgress,
    ProjectTimeline,
    ProjectTask,
    ProjectVersion,
    Notification,
    Invoice,
    Contract,
    Review,
)

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            "full_name",
            "company",
            "phone",
            "email",
            "website",
            "telegram",
            "service",
            "budget",
            "deadline",
            "description",
            "attachment",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "نام و نام خانوادگی",
                }
            ),

            "company": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "نام شرکت (اختیاری)",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "شماره تماس (09xxxxxxxxx)",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "ایمیل (اختیاری)",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "https://example.com",
                }
            ),

            "telegram": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "@username",
                }
            ),

            "service": forms.Select(
                attrs={
                    "class": "form-select form-select-lg",
                }
            ),

            "budget": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "بودجه تقریبی (تومان)",
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "type": "date",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "مثال: طراحی سایت فروشگاهی با پنل مدیریت، درگاه پرداخت و طراحی اختصاصی...",
                }
            ),
        }

    def clean_full_name(self):

        name = self.cleaned_data["full_name"].strip()

        if len(name) < 3:
            raise forms.ValidationError("نام باید حداقل ۳ کاراکتر باشد.")

        if len(name) > 100:
            raise forms.ValidationError("نام بیش از حد طولانی است.")

        return name

    def clean_description(self):

        description = self.cleaned_data["description"]

        if len(description.strip()) < 20:
            raise forms.ValidationError(
                "توضیحات پروژه باید حداقل ۲۰ کاراکتر باشد."
            )

        return description

    def clean_phone(self):

        phone = self.cleaned_data["phone"].replace(" ", "")

        pattern = r"^09\d{9}$"

        if not re.match(pattern, phone):
            raise forms.ValidationError(
                "شماره موبایل معتبر نیست."
            )

        return phone

    def clean_email(self):

        email = self.cleaned_data["email"]

        if email:

            email = email.lower()

            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("ایمیل معتبر نیست.")

        return email

    def clean_budget(self):

        budget = self.cleaned_data.get("budget")

        if budget and budget < 1_000_000:
            raise forms.ValidationError(
                "حداقل بودجه باید یک میلیون تومان باشد."
            )

        return budget

    def clean_attachment(self):

        file = self.cleaned_data.get("attachment")

        if not file:
            return file

        if file.size > 20 * 1024 * 1024:
            raise forms.ValidationError(
                "حجم فایل نباید بیشتر از 20 مگابایت باشد."
            )

        return file

class ContactForm(forms.ModelForm):

    class Meta:

        model = Contact

        fields = [

            "full_name",

            "email",

            "subject",

            "message",

        ]

        widgets = {

            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام شما"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل"
            }),

            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "موضوع"
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "پیام شما..."
            }),

        }
class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            "career",
            "full_name",
            "email",
            "phone",
            "city",
            "age",
            "experience",
            "github",
            "linkedin",
            "portfolio",
            "website",
            "resume",
            "cover_letter",
        ]

        widgets = {
            "career": forms.Select(attrs={"class": "form-select"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "experience": forms.TextInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "resume": forms.FileInput(attrs={"class": "form-control"}),
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
        }

class TicketForm(forms.ModelForm):

    class Meta:

        model = Ticket

        fields = (
            "message",
            "attachment",
        )

        widgets = {

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "پیام خود را بنویسید...",
                }
            ),

            "attachment": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),

        }

class ProjectProgressForm(forms.ModelForm):

    class Meta:

        model = ProjectProgress

        fields = (
            "title",
            "description",
            "progress",
            "completed",
            "is_visible_to_client",
        )

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "عنوان مرحله",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "توضیحات",
                }
            ),

            "progress": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                }
            ),
        }

class InvoiceForm(forms.ModelForm):

    class Meta:

        model = Invoice

        fields = (
            "amount",
            "due_date",
            "status",
        )

        widgets = {

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

        }

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {

            "rating": forms.Select(
                choices=[
                    (1, "⭐"),
                    (2, "⭐⭐"),
                    (3, "⭐⭐⭐"),
                    (4, "⭐⭐⭐⭐"),
                    (5, "⭐⭐⭐⭐⭐"),
                ],
                attrs={
                    "class": "form-select",
                },
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "نظر خود را بنویسید...",
                }
            ),
        }

class ProjectTimelineForm(forms.ModelForm):

    class Meta:

        model = ProjectTimeline

        fields = "__all__"

class ProjectTaskForm(forms.ModelForm):

    class Meta:

        model = ProjectTask

        fields = "__all__"

class ProjectVersionForm(forms.ModelForm):

    class Meta:

        model = ProjectVersion

        fields = "__all__"

class NotificationForm(forms.ModelForm):

    class Meta:

        model = Notification

        fields = "__all__"

class InvoiceForm(forms.ModelForm):

    class Meta:

        model = Invoice

        fields = "__all__"

class ContractForm(forms.ModelForm):

    class Meta:

        model = Contract

        fields = "__all__"
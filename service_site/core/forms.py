from django import forms
from django.core.validators import RegexValidator
from django.utils import timezone
import re

from .models import (
    ContactMessage,
    Order,
    JobApplication,
    Ticket,
    Review,
    Timeline,
    ProjectTask,
    ProjectProgress,
    VersionHistory,
    Notification,
    Payment,
    Report,
    Invoice,
    CompanySetting,
    SupportTicket,
    Contract,
    Service,
)

phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره موبایل معتبر نیست.",
)

class BaseStyledForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.setdefault(
                "class",
                "form-control",
            )

            field.widget.attrs.setdefault(
                "autocomplete",
                "off",
            )

class DateInput(forms.DateInput):

    input_type = "date"

class DateTimeInput(forms.DateTimeInput):

    input_type = "datetime-local"

class LargeTextarea(forms.Textarea):

    def __init__(self, *args, **kwargs):

        kwargs.setdefault(
            "attrs",
            {
                "rows": 6,
                "class": "form-control",
            },
        )

        super().__init__(*args, **kwargs)

# ==========================================================
# CONTACT FORM
# ==========================================================

class ContactForm(BaseStyledForm):

    phone = forms.CharField(

        label="شماره تماس",

        validators=[phone_validator],

        max_length=11,

    )

    class Meta:

        model = ContactMessage

        fields = [

            "name",

            "email",

            "phone",

            "subject",

            "message",

        ]

        widgets = {

            "name": forms.TextInput(

                attrs={

                    "placeholder": "نام و نام خانوادگی",

                }

            ),

            "email": forms.EmailInput(

                attrs={

                    "placeholder": "example@email.com",

                }

            ),

            "phone": forms.TextInput(

                attrs={

                    "placeholder": "09123456789",

                }

            ),

            "subject": forms.TextInput(

                attrs={

                    "placeholder": "موضوع پیام",

                }

            ),

            "message": LargeTextarea(

                attrs={

                    "rows": 6,

                    "placeholder": "پیام خود را بنویسید...",

                }

            ),

        }

    def clean_name(self):

        name = self.cleaned_data["name"].strip()

        if len(name) < 3:

            raise forms.ValidationError(

                "نام وارد شده معتبر نیست."

            )

        return name

    def clean_subject(self):

        subject = self.cleaned_data["subject"].strip()

        if len(subject) < 5:

            raise forms.ValidationError(

                "موضوع خیلی کوتاه است."

            )

        return subject

    def clean_message(self):

        message = self.cleaned_data["message"].strip()

        if len(message) < 15:

            raise forms.ValidationError(

                "متن پیام باید حداقل ۱۵ کاراکتر باشد."

            )

        return message

    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get("email")

        message = cleaned_data.get("message")

        if email and message:

            if email.lower() in message.lower():

                raise forms.ValidationError(

                    "ایمیل را داخل متن پیام وارد نکنید."

                )

        return cleaned_data

# ==========================================================
# ORDER FORM
# ==========================================================

class OrderForm(BaseStyledForm):

    phone = forms.CharField(

        label="شماره تماس",

        validators=[phone_validator],

        max_length=11,

    )

    class Meta:

        model = Order

        fields = [

            "service",

            "name",

            "email",

            "phone",

            "description",

            "attachment",

        ]

        widgets = {

            "service": forms.Select(),

            "name": forms.TextInput(

                attrs={

                    "placeholder": "نام و نام خانوادگی",

                }

            ),

            "email": forms.EmailInput(

                attrs={

                    "placeholder": "example@email.com",

                }

            ),

            "phone": forms.TextInput(

                attrs={

                    "placeholder": "09123456789",

                }

            ),

            "description": LargeTextarea(

                attrs={

                    "placeholder": "توضیحات کامل پروژه",

                }

            ),

        }

    def clean_service(self):

        service = self.cleaned_data["service"]

        if not service.is_active:

            raise forms.ValidationError(

                "این سرویس در حال حاضر غیرفعال است."

            )

        return service

    def clean_description(self):

        description = self.cleaned_data["description"].strip()

        if len(description) < 20:

            raise forms.ValidationError(

                "توضیحات پروژه باید حداقل ۲۰ کاراکتر باشد."

            )

        return description

    def clean_attachment(self):

        attachment = self.cleaned_data.get("attachment")

        if not attachment:

            return attachment

        if attachment.size > 20 * 1024 * 1024:

            raise forms.ValidationError(

                "حداکثر حجم فایل ۲۰ مگابایت است."

            )

        allowed = [

            ".pdf",

            ".zip",

            ".rar",

            ".doc",

            ".docx",

            ".png",

            ".jpg",

            ".jpeg",

            ".webp",

        ]

        import os

        ext = os.path.splitext(

            attachment.name

        )[1].lower()

        if ext not in allowed:

            raise forms.ValidationError(

                "فرمت فایل مجاز نیست."

            )

        return attachment

    def clean(self):

        cleaned_data = super().clean()

        service = cleaned_data.get("service")

        description = cleaned_data.get("description")

        if service and description:

            if len(description) < 30 and service.price > 1000000:

                raise forms.ValidationError(

                    "برای این سرویس توضیحات کامل‌تری وارد کنید."

                )

        return cleaned_data

# ==========================================================
# JOB APPLICATION FORM
# ==========================================================

class JobApplicationForm(BaseStyledForm):

    phone = forms.CharField(

        label="شماره تماس",

        validators=[phone_validator],

        max_length=11,

    )

    class Meta:

        model = JobApplication

        fields = [

            "full_name",

            "email",

            "phone",

            "position",

            "skills",

            "experience",

            "resume",

            "portfolio",

            "message",

        ]

        widgets = {

            "full_name": forms.TextInput(

                attrs={

                    "placeholder": "نام و نام خانوادگی",

                }

            ),

            "email": forms.EmailInput(

                attrs={

                    "placeholder": "example@email.com",

                }

            ),

            "phone": forms.TextInput(

                attrs={

                    "placeholder": "09123456789",

                }

            ),

            "position": forms.Select(),

            "skills": LargeTextarea(

                attrs={

                    "rows": 3,

                    "placeholder": "مهارت‌های خود را بنویسید",

                }

            ),

            "experience": LargeTextarea(

                attrs={

                    "rows": 4,

                    "placeholder": "سوابق کاری",

                }

            ),

            "portfolio": forms.URLInput(

                attrs={

                    "placeholder": "https://",

                }

            ),

            "message": LargeTextarea(

                attrs={

                    "rows": 5,

                    "placeholder": "توضیحات تکمیلی",

                }

            ),

        }

    def clean_full_name(self):

        value = self.cleaned_data["full_name"].strip()

        if len(value) < 3:

            raise forms.ValidationError(

                "نام معتبر نیست."

            )

        return value

    def clean_skills(self):

        skills = self.cleaned_data["skills"].strip()

        if len(skills) < 10:

            raise forms.ValidationError(

                "حداقل چند مهارت وارد کنید."

            )

        return skills

    def clean_resume(self):

        resume = self.cleaned_data.get("resume")

        if not resume:

            raise forms.ValidationError(

                "رزومه الزامی است."

            )

        import os

        ext = os.path.splitext(

            resume.name

        )[1].lower()

        allowed = [

            ".pdf",

            ".doc",

            ".docx",

        ]

        if ext not in allowed:

            raise forms.ValidationError(

                "رزومه باید PDF یا Word باشد."

            )

        if resume.size > 10 * 1024 * 1024:

            raise forms.ValidationError(

                "حداکثر حجم رزومه ۱۰ مگابایت است."

            )

        return resume

    def clean(self):

        cleaned_data = super().clean()

        portfolio = cleaned_data.get("portfolio")

        experience = cleaned_data.get("experience")

        if portfolio and not portfolio.startswith(("http://", "https://")):

            raise forms.ValidationError(

                "آدرس نمونه‌کار معتبر نیست."

            )

        if experience and len(experience.strip()) < 20:

            raise forms.ValidationError(

                "سوابق کاری را کامل‌تر بنویسید."

            )

        return cleaned_data

# ==========================================================
# TICKET FORM
# ==========================================================

class TicketForm(BaseStyledForm):

    class Meta:

        model = Ticket

        fields = [

            "department",

            "priority",

            "subject",

            "message",

            "attachment",

        ]

        widgets = {

            "department": forms.Select(),

            "priority": forms.Select(),

            "subject": forms.TextInput(

                attrs={

                    "placeholder": "موضوع تیکت",

                }

            ),

            "message": LargeTextarea(

                attrs={

                    "placeholder": "مشکل خود را کامل توضیح دهید",

                }

            ),

        }

    def clean_subject(self):

        subject = self.cleaned_data["subject"].strip()

        if len(subject) < 5:

            raise forms.ValidationError(

                "موضوع خیلی کوتاه است."

            )

        return subject

    def clean_message(self):

        message = self.cleaned_data["message"].strip()

        if len(message) < 20:

            raise forms.ValidationError(

                "متن تیکت باید حداقل ۲۰ کاراکتر باشد."

            )

        return message

    def clean_attachment(self):

        attachment = self.cleaned_data.get("attachment")

        if not attachment:

            return attachment

        import os

        ext = os.path.splitext(

            attachment.name

        )[1].lower()

        allowed = [

            ".pdf",

            ".zip",

            ".rar",

            ".png",

            ".jpg",

            ".jpeg",

            ".webp",

            ".txt",

            ".log",

        ]

        if ext not in allowed:

            raise forms.ValidationError(

                "فرمت فایل مجاز نیست."

            )

        if attachment.size > 15 * 1024 * 1024:

            raise forms.ValidationError(

                "حداکثر حجم فایل ۱۵ مگابایت است."

            )

        return attachment

    def clean(self):

        cleaned_data = super().clean()

        priority = cleaned_data.get("priority")

        message = cleaned_data.get("message")

        if (

            priority == "high"

            and len(message.strip()) < 50

        ):

            raise forms.ValidationError(

                "برای تیکت با اولویت بالا، توضیح کامل‌تری بنویسید."

            )

        return cleaned_data

# ==========================================================
# REVIEW FORM
# ==========================================================

class ReviewForm(BaseStyledForm):

    class Meta:

        model = Review

        fields = [

            "rating",

            "title",

            "comment",

        ]

        widgets = {

            "rating": forms.Select(),

            "title": forms.TextInput(

                attrs={

                    "placeholder": "عنوان نظر",

                }

            ),

            "comment": LargeTextarea(

                attrs={

                    "rows": 5,

                    "placeholder": "نظر خود را بنویسید",

                }

            ),

        }

    def clean_title(self):

        title = self.cleaned_data["title"].strip()

        if len(title) < 3:

            raise forms.ValidationError(

                "عنوان خیلی کوتاه است."

            )

        return title

    def clean_comment(self):

        comment = self.cleaned_data["comment"].strip()

        if len(comment) < 10:

            raise forms.ValidationError(

                "نظر باید حداقل ۱۰ کاراکتر باشد."

            )

        return comment

# ==========================================================
# PROJECT TIMELINE FORM
# ==========================================================

class TimelineForm(BaseStyledForm):

    class Meta:

        model = Timeline

        fields = [

            "title",

            "description",

            "start_date",

            "end_date",

        ]

        widgets = {

            "title": forms.TextInput(),

            "description": LargeTextarea(),

            "start_date": DateInput(),

            "end_date": DateInput(),

        }

    def clean(self):

        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")

        end = cleaned_data.get("end_date")

        if start and end and end < start:

            raise forms.ValidationError(

                "تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد."

            )

        return cleaned_data

# ==========================================================
# PROJECT TASK FORM
# ==========================================================

class ProjectTaskForm(BaseStyledForm):

    class Meta:

        model = ProjectTask

        fields = [

            "title",

            "description",

            "deadline",

            "status",

            "assigned_to",

        ]

        widgets = {

            "title": forms.TextInput(),

            "description": LargeTextarea(),

            "deadline": DateInput(),

            "status": forms.Select(),

            "assigned_to": forms.Select(),

        }

    def clean_deadline(self):

        deadline = self.cleaned_data.get("deadline")

        if deadline and deadline < timezone.now().date():

            raise forms.ValidationError(

                "ددلاین نمی‌تواند در گذشته باشد."

            )

        return deadline

# ==========================================================
# PROJECT PROGRESS FORM
# ==========================================================

class ProjectProgressForm(BaseStyledForm):

    class Meta:

        model = ProjectProgress

        fields = [

            "project",

            "percentage",

            "note",

        ]

        widgets = {

            "project": forms.Select(),

            "percentage": forms.NumberInput(

                attrs={

                    "min": 0,

                    "max": 100,

                }

            ),

            "note": LargeTextarea(

                attrs={

                    "rows": 4,

                }

            ),

        }

    def clean_percentage(self):

        value = self.cleaned_data["percentage"]

        if value < 0 or value > 100:

            raise forms.ValidationError(

                "درصد باید بین ۰ تا ۱۰۰ باشد."

            )

        return value

# ==========================================================
# PROJECT VERSION FORM
# ==========================================================

class VersionHistoryForm(BaseStyledForm):

    class Meta:

        model = VersionHistory

        fields = [
            "project",
            "version",
            "changes",
        ]

        widgets = {

            "project": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "version": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثلا v1.0.0",
                }
            ),

            "changes": LargeTextarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "تغییرات این نسخه را کامل توضیح دهید",
                }
            ),
        }


    def clean_version(self):

        version = self.cleaned_data.get("version")

        if not version:
            raise forms.ValidationError(
                "شماره نسخه الزامی است."
            )

        version = version.strip()

        if len(version) < 2:
            raise forms.ValidationError(
                "شماره نسخه معتبر نیست."
            )

        return version


    def clean_changes(self):

        changes = self.cleaned_data.get("changes")

        if not changes:
            raise forms.ValidationError(
                "توضیحات تغییرات الزامی است."
            )

        changes = changes.strip()

        if len(changes) < 10:
            raise forms.ValidationError(
                "توضیحات تغییرات باید حداقل ۱۰ کاراکتر باشد."
            )

        return changes


    def clean(self):

        cleaned_data = super().clean()

        project = cleaned_data.get("project")
        version = cleaned_data.get("version")

        if project and version:

            exists = VersionHistory.objects.filter(
                project=project,
                version=version
            ).exists()

            if exists:

                raise forms.ValidationError(
                    "این نسخه قبلا برای این پروژه ثبت شده است."
                )

        return cleaned_data

# ==========================================================
# NOTIFICATION FORM
# ==========================================================

class NotificationForm(BaseStyledForm):

    class Meta:

        model = Notification

        fields = [

            "user",

            "title",

            "message",

            "related_url",

            "notification_type",

        ]

        widgets = {

            "user": forms.Select(),

            "title": forms.TextInput(),

            "message": LargeTextarea(

                attrs={

                    "rows": 4,

                }

            ),

            "link": forms.URLInput(),

        }

    def clean_message(self):

        message = self.cleaned_data["message"].strip()

        if len(message) < 5:

            raise forms.ValidationError(

                "متن اعلان خیلی کوتاه است."

            )

        return message

    def clean_link(self):

        link = self.cleaned_data.get("link")

        if not link:

            return link

        return link.strip()

# ==========================================================
# PAYMENT FORM
# ==========================================================

class PaymentForm(BaseStyledForm):

    class Meta:

        model = Payment

        fields = [

            "order",

            "amount",

            "gateway",

            "status",

            "transaction_id",

        ]

        widgets = {

            "order": forms.Select(),

            "amount": forms.NumberInput(

                attrs={

                    "min": 0,

                }

            ),

            "gateway": forms.TextInput(),

            "status": forms.Select(),

            "transaction_id": forms.TextInput(),

        }

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        if amount <= 0:

            raise forms.ValidationError(

                "مبلغ پرداخت باید بیشتر از صفر باشد."

            )

        return amount

    def clean_transaction_id(self):

        value = self.cleaned_data["transaction_id"].strip()

        if len(value) < 5:

            raise forms.ValidationError(

                "شناسه تراکنش معتبر نیست."

            )

        return value

# ==========================================================
# INVOICE FORM
# ==========================================================

class InvoiceForm(BaseStyledForm):

    class Meta:

        model = Invoice

        fields = [

            "order",

            "amount",

            "status",

            "pdf",

        ]

        widgets = {

            "order": forms.Select(),

            "invoice_number": forms.TextInput(),

            "amount": forms.NumberInput(),

            "status": forms.Select(),

        }

    def clean_invoice_number(self):

        number = self.cleaned_data["invoice_number"].strip()

        if len(number) < 3:

            raise forms.ValidationError(

                "شماره فاکتور معتبر نیست."

            )

        return number

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        if amount <= 0:

            raise forms.ValidationError(

                "مبلغ فاکتور نامعتبر است."

            )

        return amount

# ==========================================================
# REPORT FORM
# ==========================================================

class ReportForm(BaseStyledForm):

    class Meta:

        model = Report

        fields = [

            "title",

            "description",

            "file",

        ]

        widgets = {

            "title": forms.TextInput(),

            "description": LargeTextarea(),

        }

    def clean_title(self):

        title = self.cleaned_data["title"].strip()

        if len(title) < 3:

            raise forms.ValidationError(

                "عنوان گزارش کوتاه است."

            )

        return title

    def clean_description(self):

        description = self.cleaned_data["description"].strip()

        if len(description) < 10:

            raise forms.ValidationError(

                "توضیحات گزارش کامل نیست."

            )

        return description

# ==========================================================
# COMPANY SETTINGS FORM
# ==========================================================

class CompanySettingForm(BaseStyledForm):

    class Meta:

        model = CompanySetting

        fields = [

            "company_name",

            "email",

            "phone",

            "address",

            "logo",

            "favicon",

            "about",

        ]

        widgets = {

            "company_name": forms.TextInput(),

            "email": forms.EmailInput(),

            "phone": forms.TextInput(),

            "address": LargeTextarea(),

            "about": LargeTextarea(),

        }

    def clean_company_name(self):

        value = self.cleaned_data["company_name"].strip()

        if len(value) < 2:

            raise forms.ValidationError(

                "نام شرکت معتبر نیست."

            )

        return value

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        phone = re.sub(r"\D", "", phone)

        if len(phone) < 10:

            raise forms.ValidationError(

                "شماره تماس معتبر نیست."

            )

        return phone
    
# ==========================================================
# NOTIFICATION FORM
# ==========================================================

class NotificationForm(BaseStyledForm):

    class Meta:

        model = Notification

        fields = [

            "user",

            "title",

            "message",

            "is_read",

        ]

        widgets = {

            "user": forms.Select(),

            "title": forms.TextInput(),

            "message": LargeTextarea(),

        }

    def clean_title(self):

        value = self.cleaned_data["title"].strip()

        if len(value) < 3:

            raise forms.ValidationError(

                "عنوان اعلان کوتاه است."

            )

        return value

    def clean_message(self):

        value = self.cleaned_data["message"].strip()

        if len(value) < 5:

            raise forms.ValidationError(

                "متن اعلان خالی است."

            )

        return value

# ==========================================================
# SUPPORT TICKET FORM
# ==========================================================

class SupportTicketForm(BaseStyledForm):

    class Meta:

        model = SupportTicket

        fields = [

            "subject",

            "message",

            "status",

            "priority",

        ]

        widgets = {

            "subject": forms.TextInput(),

            "message": LargeTextarea(),

            "status": forms.Select(),

            "priority": forms.Select(),

        }

    def clean_subject(self):

        value = self.cleaned_data["subject"].strip()

        if len(value) < 5:

            raise forms.ValidationError(

                "موضوع تیکت کوتاه است."

            )

        return value

    def clean_message(self):

        value = self.cleaned_data["message"].strip()

        if len(value) < 10:

            raise forms.ValidationError(

                "متن تیکت کامل نیست."

            )

        return value

# ==========================================================
# SEARCH FORM
# ==========================================================

class SearchForm(forms.Form):

    query = forms.CharField(

        max_length=150,

        required=False,

        widget=forms.TextInput(

            attrs={

                "placeholder": "جستجو...",

            }

        ),

    )

    def clean_query(self):

        query = self.cleaned_data["query"].strip()

        if len(query) > 150:

            raise forms.ValidationError(

                "عبارت جستجو بیش از حد طولانی است."

            )

        return query

# ==========================================================
# CONTACT FORM
# ==========================================================

class ContactForm(forms.Form):

    name = forms.CharField(

        max_length=100,

    )

    email = forms.EmailField()

    subject = forms.CharField(

        max_length=150,

    )

    message = forms.CharField(

        widget=LargeTextarea(),

    )

    def clean_name(self):

        value = self.cleaned_data["name"].strip()

        if len(value) < 2:

            raise forms.ValidationError(

                "نام معتبر نیست."

            )

        return value

    def clean_subject(self):

        value = self.cleaned_data["subject"].strip()

        if len(value) < 3:

            raise forms.ValidationError(

                "موضوع معتبر نیست."

            )

        return value

    def clean_message(self):

        value = self.cleaned_data["message"].strip()

        if len(value) < 10:

            raise forms.ValidationError(

                "متن پیام خیلی کوتاه است."

            )

        return value

# ==========================================================
# NEWSLETTER FORM
# ==========================================================

class NewsletterForm(forms.Form):

    email = forms.EmailField()

    def clean_email(self):

        email = self.cleaned_data["email"].lower()

        return email

# ==========================================================
# FILE VALIDATORS
# ==========================================================

def validate_pdf(file):

    if not file.name.lower().endswith(".pdf"):

        raise forms.ValidationError(

            "فقط فایل PDF مجاز است."

        )

    return file

def validate_image(file):

    allowed = [

        ".jpg",

        ".jpeg",

        ".png",

        ".webp",

    ]

    if not any(

        file.name.lower().endswith(ext)

        for ext in allowed

    ):

        raise forms.ValidationError(

            "فرمت تصویر مجاز نیست."

        )

    return file

# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "ServiceForm",

    "PortfolioForm",

    "OrderForm",

    "CategoryForm",

    "BlogCategoryForm",

    "BlogPostForm",

    "CommentForm",

    "TagForm",

    "EmployeeForm",

    "DepartmentForm",

    "TimelineForm",

    "FAQForm",

    "PaymentForm",

    "InvoiceForm",

    "ReportForm",

    "NotificationForm",

    "SupportTicketForm",

    "CompanySettingForm",

    "SearchForm",

    "ContactForm",

    "NewsletterForm",

]
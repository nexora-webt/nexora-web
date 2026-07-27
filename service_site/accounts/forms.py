# ==========================================================
# IMPORTS
# ==========================================================

from django import forms

from django.core.exceptions import ValidationError

import re

# ==========================================================
# BASE FORM
# ==========================================================
class BaseForm(forms.Form):

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.add_css_classes()

    def add_css_classes(self):


        for field_name in self.fields:


            field = self.fields[field_name]


            field.widget.attrs.update({

                "class": "form-control",

            })
# ==========================================================
# BASE MODEL FORM
# ==========================================================
class BaseModelForm(forms.ModelForm):

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.add_css_classes()

    def add_css_classes(self):

        for field_name in self.fields:


            field = self.fields[field_name]


            field.widget.attrs.update({

                "class": "form-control",

            })
# ==========================================================
# MIXINS
# ==========================================================
class BootstrapMixin:

    def apply_bootstrap(self):

        for field_name in self.fields:

            self.fields[field_name].widget.attrs.update({

                "class": "form-control",

            })

class DisableFieldsMixin:

    def disable_fields(
        self,
        fields
    ):

        for field_name in fields:

            if field_name in self.fields:

                self.fields[field_name].disabled = True

class ReadOnlyFieldsMixin:

    def make_readonly(
        self,
        fields
    ):

        for field_name in fields:

            if field_name in self.fields:

                self.fields[field_name].widget.attrs.update({

                    "readonly": True,
                })
# ==========================================================
# COMMON VALIDATORS
# ==========================================================
# --------------------------
# Phone Validator
# --------------------------
def validate_phone(value):

    pattern = r"^09\d{9}$"

    if not re.match(
        pattern,
        value
    ):

        raise ValidationError(

            "شماره موبایل معتبر نیست."
        )
# --------------------------
# Username Validator
# --------------------------
def validate_username(value):

    if not re.match(
        r"^[a-zA-Z0-9_]+$",
        value
    ):

        raise ValidationError(

            "نام کاربری فقط می‌تواند شامل حروف، عدد و _ باشد."
        )
# --------------------------
# Strong Password Validator
# --------------------------
def validate_strong_password(value):

    errors = []

    if len(value) < 8:

        errors.append(

            "رمز عبور باید حداقل ۸ کاراکتر باشد."
        )

    if not re.search(
        r"[A-Z]",
        value
    ):

        errors.append(

            "رمز عبور باید حداقل یک حرف بزرگ داشته باشد."
        )

    if not re.search(
        r"[a-z]",
        value
    ):

        errors.append(

            "رمز عبور باید حداقل یک حرف کوچک داشته باشد."
        )

    if not re.search(
        r"[0-9]",
        value
    ):

        errors.append(

            "رمز عبور باید حداقل یک عدد داشته باشد."
        )

    if errors:

        raise ValidationError(
            errors
        )
# --------------------------
# File Size Validator
# --------------------------
def validate_file_size(file):

    max_size = 5 * 1024 * 1024

    if file.size > max_size:

        raise ValidationError(

            "حجم فایل نباید بیشتر از ۵ مگابایت باشد."
        )
# --------------------------
# Image Extension Validator
# --------------------------
def validate_image_extension(file):

    allowed_extensions = [

        "jpg",

        "jpeg",

        "png",

        "webp",
    ]

    extension = file.name.split(".")[-1].lower()

    if extension not in allowed_extensions:

        raise ValidationError(

            "فرمت تصویر مجاز نیست."
        )
# ==========================================================
# IMPORTS
# ==========================================================

from django.contrib.auth.models import User

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)


# ==========================================================
# REGISTER FORM
# ==========================================================


class RegisterForm(
    UserCreationForm
):


    email = forms.EmailField(

        required=True,

        widget=forms.EmailInput(

            attrs={

                "class": "form-control",

                "placeholder": "ایمیل",

            }

        )

    )



    username = forms.CharField(

        max_length=150,

        validators=[

            validate_username,

        ],

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "نام کاربری",

            }

        )

    )



    password1 = forms.CharField(

        validators=[

            validate_strong_password,

        ],

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "رمز عبور",

            }

        )

    )



    password2 = forms.CharField(

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "تکرار رمز عبور",

            }

        )

    )



    class Meta:


        model = User


        fields = [

            "username",

            "email",

            "password1",

            "password2",

        ]



    # --------------------------------------
    # Email Validation
    # --------------------------------------


    def clean_email(self):


        email = self.cleaned_data.get(

            "email"

        )


        if User.objects.filter(

            email=email

        ).exists():


            raise ValidationError(

                "این ایمیل قبلاً ثبت شده است."

            )


        return email



    # --------------------------------------
    # Username Validation
    # --------------------------------------


    def clean_username(self):


        username = self.cleaned_data.get(

            "username"

        )


        validate_username(

            username

        )


        if User.objects.filter(

            username=username

        ).exists():


            raise ValidationError(

                "این نام کاربری قبلاً استفاده شده است."

            )


        return username



# ==========================================================
# LOGIN FORM
# ==========================================================


class LoginForm(

    AuthenticationForm

):


    username = forms.CharField(

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "نام کاربری",

            }

        )

    )



    password = forms.CharField(

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "رمز عبور",

            }

        )

    )



    error_messages = {

        "invalid_login":

            "نام کاربری یا رمز عبور اشتباه است.",


        "inactive":

            "حساب کاربری شما فعال نیست.",

    }

from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from django.contrib.auth.models import User


class VerifyEmailForm(forms.Form):

    email = forms.EmailField(

        widget=forms.EmailInput(

            attrs={

                "class": "form-control",

                "placeholder": "ایمیل",

            }

        )

    )



    def clean_email(self):

        email = self.cleaned_data.get(
            "email"
        )


        if not User.objects.filter(
            email=email
        ).exists():

            raise ValidationError(
                "کاربری با این ایمیل وجود ندارد."
            )


        return email



class PasswordResetRequestForm(
    PasswordResetForm
):


    email = forms.EmailField(

        widget=forms.EmailInput(

            attrs={

                "class": "form-control",

                "placeholder": "ایمیل حساب کاربری",

            }

        )

    )



    def clean_email(self):

        email = self.cleaned_data.get(
            "email"
        )


        if not User.objects.filter(
            email=email
        ).exists():

            raise ValidationError(
                "این ایمیل ثبت نشده است."
            )


        return email



class PasswordResetConfirmForm(
    SetPasswordForm
):


    new_password1 = forms.CharField(

        validators=[

            validate_strong_password,

        ],

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



class ChangePasswordForm(
    PasswordChangeForm
):


    old_password = forms.CharField(

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "رمز عبور فعلی",

            }

        )

    )



    new_password1 = forms.CharField(

        validators=[

            validate_strong_password,

        ],

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

from .models import UserProfile


class ProfileForm(
    BaseModelForm
):


    class Meta:

        model = UserProfile


        fields = [

            "avatar",

            "phone",

            "bio",

        ]


        widgets = {


            "avatar": forms.FileInput(

                attrs={

                    "class": "form-control",

                }

            ),


            "phone": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "شماره تماس",

                }

            ),


            "bio": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 5,

                    "placeholder": "درباره خودتان",

                }

            ),

        }



    def clean_phone(self):


        phone = self.cleaned_data.get(

            "phone"

        )


        if phone:


            validate_phone(

                phone

            )


        return phone



    def clean_avatar(self):


        avatar = self.cleaned_data.get(

            "avatar"

        )


        if avatar:


            validate_file_size(

                avatar

            )


            validate_image_extension(

                avatar

            )


        return avatar

from .models import Address


class AddressForm(
    BaseModelForm
):


    class Meta:

        model = Address


        fields = [

            "title",

            "full_name",

            "phone",

            "province",

            "city",

            "address",

            "postal_code",

            "is_default",

        ]


        widgets = {


            "title": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "عنوان آدرس",

                }

            ),


            "full_name": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "نام کامل",

                }

            ),


            "phone": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "شماره تماس",

                }

            ),


            "province": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "استان",

                }

            ),


            "city": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "شهر",

                }

            ),


            "address": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "آدرس کامل",

                }

            ),


            "postal_code": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "کد پستی",

                }

            ),


            "is_default": forms.CheckboxInput(

                attrs={

                    "class": "form-check-input",

                }

            ),

        }



    def clean_phone(self):


        phone = self.cleaned_data.get(

            "phone"

        )


        validate_phone(

            phone

        )


        return phone



    def clean_postal_code(self):


        postal_code = self.cleaned_data.get(

            "postal_code"
        )

        if not postal_code.isdigit() or len(postal_code) != 10:

            raise ValidationError(

                "کد پستی باید ۱۰ رقم باشد."
            )

        return postal_code

from core.models import Ticket, TicketReply, TicketAttachment

class TicketForm(
    BaseModelForm
):

    class Meta:

        model = Ticket

        fields = [

            "subject",

            "category",

            "priority",

            "message",

        ]


        widgets = {


            "subject": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "عنوان درخواست",

                }

            ),


            "category": forms.Select(

                attrs={

                    "class": "form-select",

                }

            ),


            "priority": forms.Select(

                attrs={

                    "class": "form-select",

                }

            ),


            "message": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 6,

                    "placeholder": "توضیحات درخواست",

                }

            ),

        }



    def clean_subject(self):


        subject = self.cleaned_data.get(

            "subject"

        )


        if len(subject) < 5:


            raise ValidationError(

                "عنوان تیکت باید حداقل ۵ کاراکتر باشد."

            )


        return subject



class TicketReplyForm(
    BaseModelForm
):


    class Meta:

        model = TicketReply


        fields = [

            "message",

        ]


        widgets = {


            "message": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 5,

                    "placeholder": "پاسخ خود را بنویسید",

                }

            ),

        }



class TicketAttachmentForm(
    BaseModelForm
):


    class Meta:

        model = TicketAttachment


        fields = [

            "file",

        ]


        widgets = {


            "file": forms.FileInput(

                attrs={

                    "class": "form-control",

                }

            ),

        }



    def clean_file(self):


        file = self.cleaned_data.get(

            "file"

        )


        if file:


            validate_file_size(

                file

            )


        return file

from .models import NotificationSettings


class NotificationSettingsForm(
    BaseModelForm
):


    class Meta:

        model = NotificationSettings


        fields = [

            "email_notifications",

            "security_alerts",

            "order_updates",

            "marketing_emails",

        ]


        widgets = {


            "email_notifications": forms.CheckboxInput(

                attrs={

                    "class": "form-check-input",

                }

            ),


            "security_alerts": forms.CheckboxInput(

                attrs={

                    "class": "form-check-input",

                }

            ),


            "order_updates": forms.CheckboxInput(

                attrs={

                    "class": "form-check-input",

                }

            ),


            "marketing_emails": forms.CheckboxInput(

                attrs={

                    "class": "form-check-input",

                }

            ),

        }



class SearchForm(
    BaseForm
):


    query = forms.CharField(

        required=False,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "جستجو در Nexora Web",

            }

        )

    )



    category = forms.ChoiceField(

        required=False,

        choices=[

            ("all", "همه"),

            ("services", "خدمات"),

            ("portfolio", "نمونه کارها"),

            ("orders", "سفارش‌ها"),

        ],

        widget=forms.Select(

            attrs={

                "class": "form-select",

            }

        )

    )



    def clean_query(self):


        query = self.cleaned_data.get(

            "query"

        )


        if query:


            query = query.strip()



            if len(query) < 2:


                raise ValidationError(

                    "عبارت جستجو کوتاه است."

                )
        return query

class ContactForm(
    BaseForm
):

    name = forms.CharField(

        max_length=100,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "نام شما",

            }

        )

    )

    email = forms.EmailField(

        widget=forms.EmailInput(

            attrs={

                "class": "form-control",

                "placeholder": "ایمیل",

            }

        )

    )

    phone = forms.CharField(

        required=False,

        validators=[

            validate_phone,

        ],

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "شماره تماس",

            }

        )

    )

    subject = forms.CharField(

        max_length=200,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "موضوع پیام",
            }
        )
    )

    message = forms.CharField(

        widget=forms.Textarea(

            attrs={

                "class": "form-control",

                "rows": 6,

                "placeholder": "پیام شما",
            }
        )
    )

    def clean_message(self):

        message = self.cleaned_data.get(

            "message"
        )

        if len(message.strip()) < 10:

            raise ValidationError(

                "متن پیام خیلی کوتاه است."
            )
        return message

from .models import (
    Department,
    Employee,
)

class DepartmentForm(
    BaseModelForm
):

    class Meta:

        model = Department

        fields = [

            "name",

            "department_type",

            "description",

            "manager",

            "icon",

            "order",
        ]

        widgets = {

            "name": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "نام دپارتمان",
                }
            ),

            "department_type": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "توضیحات دپارتمان",
                }
            ),

            "manager": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "icon": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "آیکون FontAwesome",
                }
            ),

            "order": forms.NumberInput(

                attrs={

                    "class": "form-control",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data.get(

            "name"
        )

        if len(name.strip()) < 3:

            raise ValidationError(

                "نام دپارتمان کوتاه است."
            )

        return name

class EmployeeForm(
    BaseModelForm
):

    class Meta:

        model = Employee

        fields = [

            "user",

            "department",

            "position",

            "skills",

            "github",

            "linkedin",

            "is_available",
        ]

        widgets = {

            "user": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "department": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "position": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "سمت کاری",
                }
            ),

            "skills": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "مهارت‌ها",
                }
            ),

            "github": forms.URLInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "لینک GitHub",
                }
            ),

            "linkedin": forms.URLInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "لینک LinkedIn",
                }
            ),

            "is_available": forms.CheckboxInput(

                attrs={

                    "class": "form-check-input",
                }
            ),
        }

    def clean_position(self):

        position = self.cleaned_data.get(

            "position"
        )

        if len(position.strip()) < 3:

            raise ValidationError(

                "عنوان شغلی معتبر نیست."

            )
        return position

from core.models import (
    Invoice,
    Payment,
)

class InvoiceForm(
    BaseModelForm
):

    class Meta:

        model = Invoice

        fields = [

            "order",

            "amount",

            "status",

            "description",
        ]

        widgets = {

            "order": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "amount": forms.NumberInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "مبلغ فاکتور",
                }
            ),

            "status": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "توضیحات فاکتور",
                }
            ),
        }

    def clean_amount(self):

        amount = self.cleaned_data.get(

            "amount"

        )

        if amount <= 0:

            raise ValidationError(

                "مبلغ فاکتور باید بیشتر از صفر باشد."
            )

        return amount

class PaymentForm(
    BaseModelForm
):

    class Meta:

        model = Payment

        fields = [

            "invoice",

            "payment_method",

            "transaction_id",

            "amount",

            "status",
        ]

        widgets = {

            "invoice": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "payment_method": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),

            "transaction_id": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "کد تراکنش",
                }
            ),

            "amount": forms.NumberInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "مبلغ پرداخت",
                }
            ),

            "status": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),
        }

    def clean_transaction_id(self):

        transaction_id = self.cleaned_data.get(

            "transaction_id"
        )

        if transaction_id:

            transaction_id = transaction_id.strip()

            if len(transaction_id) < 5:

                raise ValidationError(

                    "کد تراکنش معتبر نیست."
                )
        return transaction_id

from accounts.models import (
    Timeline,
    ProjectProgress,
    VersionHistory,
)

class TimelineForm(
    BaseModelForm
):

    class Meta:

        model = Timeline

        fields = [

            "title",

            "description",

            "status",
        ]

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

                    "placeholder": "توضیحات مرحله",
                }
            ),

            "status": forms.Select(

                attrs={

                    "class": "form-select",
                }
            ),
        }

class ProjectProgressForm(
    BaseModelForm
):

    class Meta:

        model = ProjectProgress

        fields = [
            "user",
            "project_name",
            "progress",
            "current_step",
            "status",
        ]

        widgets = {

            "percentage": forms.NumberInput(

                attrs={

                    "class": "form-control",

                    "min": 0,

                    "max": 100,

                    "placeholder": "درصد پیشرفت",
                }
            ),

            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "توضیحات پیشرفت پروژه",
                }
            ),
        }

    def clean_percentage(self):

        percentage = self.cleaned_data.get(

            "percentage"
        )

        if percentage < 0 or percentage > 100:

            raise ValidationError(

                "درصد پیشرفت باید بین ۰ تا ۱۰۰ باشد."
            )

        return percentage

class VersionHistoryForm(
    BaseModelForm
):

    class Meta:

        model = VersionHistory

        fields = [
            "version",
            "title",
            "description",
            "released_at",
            "is_stable",
        ]

        widgets = {

            "version": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "نسخه پروژه",
                }
            ),

            "title": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "عنوان نسخه",
                }
            ),

            "description": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 4,

                    "placeholder": "توضیحات تغییرات",
                }
            ),

            "file": forms.FileInput(

                attrs={

                    "class": "form-control",
                }
            ),
        }

    def clean_file(self):

        file = self.cleaned_data.get(

            "file"
        )

        if file:

            validate_file_size(

                file
            )

        return file

import os

from django.utils.html import strip_tags

def clean_text(value):

    if not value:

        return value

    value = strip_tags(value)

    value = value.strip()

    return value

def validate_safe_file(file):

    allowed_extensions = [

        ".jpg",

        ".jpeg",

        ".png",

        ".webp",

        ".pdf",

        ".zip",
    ]

    extension = os.path.splitext(

        file.name

    )[1].lower()

    if extension not in allowed_extensions:

        raise ValidationError(

            "این نوع فایل مجاز نیست."
        )

    max_size = 10 * 1024 * 1024

    if file.size > max_size:

        raise ValidationError(

            "حجم فایل نباید بیشتر از ۱۰ مگابایت باشد."
        )

def validate_no_spam(value):

    spam_words = [

        "http://",

        "https://",

        "www.",

        "<script",

        "javascript:",
    ]

    text = value.lower()

    for word in spam_words:

        if word in text:

            raise ValidationError(

                "متن وارد شده معتبر نیست."
            )

    return value

class SecurityValidationMixin:

    def clean_fields(self):

        cleaned_data = super().clean_fields()

        for field_name, value in cleaned_data.items():

            if isinstance(value, str):

                cleaned_data[field_name] = clean_text(

                    value
                )

        return cleaned_data

class SecureFileMixin:

    def clean_file_field(

        self,

        field_name="file"
    ):

        file = self.cleaned_data.get(

            field_name
        )

        if file:

            validate_safe_file(

                file
            )

        return file

FORM_CONTROL_CLASS = "form-control"

FORM_SELECT_CLASS = "form-select"

FORM_CHECKBOX_CLASS = "form-check-input"

__all__ = [

    "RegisterForm",

    "LoginForm",

    "VerifyEmailForm",

    "PasswordResetRequestForm",

    "PasswordResetConfirmForm",

    "ChangePasswordForm",

    "ProfileForm",

    "AddressForm",

    "TicketForm",

    "TicketReplyForm",

    "TicketAttachmentForm",

    "NotificationSettingsForm",

    "SearchForm",

    "ContactForm",

    "DepartmentForm",

    "EmployeeForm",

    "InvoiceForm",

    "PaymentForm",

    "TimelineForm",

    "ProjectProgressForm",

    "VersionHistoryForm",

]
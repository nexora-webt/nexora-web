# ==========================================================
# IMPORTS
# ==========================================================
import os
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# ==========================================================
# CONSTANTS
# ==========================================================

MAX_UPLOAD_SIZE = 20 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "webp",
    "svg",
)

ALLOWED_DOCUMENT_EXTENSIONS = (
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
    "zip",
    "rar",
    "7z",
    "txt",
)

ALLOWED_PORTFOLIO_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "webp",
    "gif",
)

# ==========================================================
# VALIDATORS
# ==========================================================

phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره موبایل معتبر نیست.",
)

english_slug_validator = RegexValidator(
    regex=r"^[a-z0-9-]+$",
    message="اسلاگ فقط می‌تواند شامل حروف انگلیسی کوچک، عدد و - باشد.",
)

username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9._]+$",
    message="نام کاربری نامعتبر است.",
)

hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="کد رنگ معتبر نیست.",
)

domain_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    message="دامنه معتبر نیست.",
)

tracking_code_validator = RegexValidator(
    regex=r"^[A-Z0-9]{10,20}$",
    message="کد پیگیری معتبر نیست.",
)

invoice_number_validator = RegexValidator(
    regex=r"^[A-Z0-9-]+$",
    message="شماره فاکتور معتبر نیست.",
)

version_validator = RegexValidator(
    regex=r"^\d+\.\d+(\.\d+)?$",
    message="فرمت نسخه باید مانند 1.0 یا 2.5.1 باشد.",
)

# ==========================================================
# FILE VALIDATORS
# ==========================================================

image_extension_validator = FileExtensionValidator(
    allowed_extensions=ALLOWED_IMAGE_EXTENSIONS,
)

document_extension_validator = FileExtensionValidator(
    allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS,
)

portfolio_extension_validator = FileExtensionValidator(
    allowed_extensions=ALLOWED_PORTFOLIO_EXTENSIONS,
)

def validate_file_size(file):

    if file.size > MAX_UPLOAD_SIZE:

        raise ValidationError(
            "حجم فایل بیشتر از 20 مگابایت است."
        )

def validate_image(file):

    validate_file_size(file)

    image_extension_validator(file)

def validate_document(file):

    validate_file_size(file)

    document_extension_validator(file)

def validate_portfolio_image(file):

    validate_file_size(file)

    portfolio_extension_validator(file)

# ==========================================================
# HELPERS
# ==========================================================

def unique_filename(filename):

    extension = os.path.splitext(filename)[1].lower()

    return f"{uuid.uuid4().hex}{extension}"


def upload_service_image(instance, filename):

    return (
        f"services/"
        f"{instance.slug}/"
        f"{unique_filename(filename)}"
    )


def upload_portfolio_cover(instance, filename):

    return (
        f"portfolio/"
        f"{instance.slug}/cover/"
        f"{unique_filename(filename)}"
    )


def upload_portfolio_gallery(instance, filename):

    return (
        f"portfolio/"
        f"{instance.portfolio.slug}/gallery/"
        f"{unique_filename(filename)}"
    )


def upload_order_file(instance, filename):

    return (
        f"orders/"
        f"{instance.order.tracking_code}/"
        f"{unique_filename(filename)}"
    )


def upload_ticket_attachment(instance, filename):

    return (
        f"tickets/"
        f"{instance.ticket.ticket_number}/"
        f"{unique_filename(filename)}"
    )


def upload_blog_image(instance, filename):

    return (
        f"blog/"
        f"{instance.slug}/"
        f"{unique_filename(filename)}"
    )


def upload_team_avatar(instance, filename):

    return (
        f"team/"
        f"{instance.user.username}/"
        f"{unique_filename(filename)}"
    )


def upload_review_avatar(instance, filename):

    return (
        f"reviews/"
        f"{unique_filename(filename)}"
    )


def upload_site_logo(instance, filename):

    return (
        f"settings/logo/"
        f"{unique_filename(filename)}"
    )


def upload_site_favicon(instance, filename):

    return (
        f"settings/favicon/"
        f"{unique_filename(filename)}"
    )


def generate_tracking_code():

    return uuid.uuid4().hex[:12].upper()


def generate_invoice_number():

    return (
        "NXW-"
        + timezone.now().strftime("%Y")
        + "-"
        + uuid.uuid4().hex[:8].upper()
    )


def generate_ticket_number():

    return (
        "TKT-"
        + timezone.now().strftime("%Y")
        + "-"
        + uuid.uuid4().hex[:8].upper()
    )


def generate_slug(text):

    slug = slugify(text)

    if not slug:

        slug = uuid.uuid4().hex[:12]

    return slug

# ==========================================================
# BASE MODEL
# ==========================================================

class BaseModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="تاریخ ایجاد",
    )


    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی",
    )


    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="فعال",
    )


    class Meta:

        abstract = True



# ==========================================================
# UUID MODEL
# ==========================================================

class UUIDModel(BaseModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="شناسه",
    )


    class Meta:

        abstract = True



# ==========================================================
# SLUG MODEL
# ==========================================================

class SlugModel(UUIDModel):

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان",
    )


    slug = models.SlugField(
        max_length=255,
        unique=True,
        validators=[
            english_slug_validator,
        ],
        verbose_name="اسلاگ",
    )


    class Meta:

        abstract = True



    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.slug:

            self.slug = generate_slug(
                self.title
            )


        super().save(
            *args,
            **kwargs
        )



    def __str__(self):

        return self.title

# ==========================================================
# CATEGORY MODEL
# ==========================================================

class Category(SlugModel):

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )


    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="آیکون",
    )


    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        validators=[
            validate_image,
        ],
        verbose_name="تصویر دسته‌بندی",
    )


    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتیب نمایش",
    )


    class Meta:

        verbose_name = "دسته‌بندی"

        verbose_name_plural = "دسته‌بندی‌ها"

        ordering = [
            "order",
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_active",
                    "order",
                ]
            ),

        ]


    def get_absolute_url(self):

        return reverse(
            "category_detail",
            kwargs={
                "slug": self.slug
            }
        )


    def __str__(self):

        return self.title

# ==========================================================
# SERVICE MODEL
# ==========================================================

class Service(SlugModel):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
        verbose_name="دسته‌بندی",
    )


    short_description = models.CharField(
        max_length=300,
        verbose_name="توضیح کوتاه",
    )


    description = models.TextField(
        verbose_name="توضیحات کامل",
    )


    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="آیکون",
    )


    image = models.ImageField(
        upload_to=upload_service_image,
        blank=True,
        null=True,
        validators=[
            validate_image,
        ],
        verbose_name="تصویر سرویس",
    )


    base_price = models.PositiveBigIntegerField(
        default=0,
        verbose_name="قیمت پایه",
    )


    max_price = models.PositiveBigIntegerField(
        default=0,
        verbose_name="حداکثر قیمت",
    )


    duration_days = models.PositiveIntegerField(
        default=7,
        verbose_name="زمان تحویل (روز)",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="سرویس ویژه",
    )


    is_available = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="قابل سفارش",
    )


    features = models.JSONField(
        default=list,
        blank=True,
        verbose_name="ویژگی‌ها",
    )


    class Meta:

        verbose_name = "سرویس"

        verbose_name_plural = "سرویس‌ها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_active",
                    "is_available",
                ]
            ),

            models.Index(
                fields=[
                    "is_featured",
                ]
            ),

        ]


    def get_absolute_url(self):

        return reverse(
            "service_detail",
            kwargs={
                "slug": self.slug
            }
        )


    def clean(self):

        if self.max_price and self.base_price > self.max_price:

            raise ValidationError(
                "قیمت پایه نمی‌تواند بیشتر از حداکثر قیمت باشد."
            )


    def __str__(self):

        return self.title

# ==========================================================
# PORTFOLIO MODEL
# ==========================================================
def upload_to_portfolio(instance, filename):
    return f"portfolio/{filename}"

def upload_to_resumes(instance, filename):
    return f"resumes/{filename}"

def upload_to_orders(instance, filename):
    return os.path.join(
        "orders/",
        filename
    )

def upload_to_versions(instance, filename):
    return os.path.join(
        "versions/",
        filename
    )

def upload_to_tickets(instance, filename):
    return os.path.join(
        "tickets/",
        filename
    )

class Portfolio(SlugModel):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portfolios",
        verbose_name="دسته‌بندی",
    )

    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portfolios",
        verbose_name="سرویس مرتبط",
    )

    live_demo_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک نسخه آنلاین",
    )

    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک GitHub",
    )

    project_duration = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="مدت انجام پروژه",
    )

    client_company = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="شرکت مشتری",
    )

    PROJECT_STATUS = (
        ("completed", "تکمیل شده"),
        ("development", "درحال توسعه"),
        ("archived", "آرشیو"),
    )

    project_status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS,
        default="completed",
        verbose_name="وضعیت پروژه",
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name="نمایش در سایت",
    )

    short_description = models.CharField(
        max_length=300,
        verbose_name="توضیح کوتاه",
    )

    views = models.PositiveIntegerField(
        default=0
    )

    description = models.TextField(
        verbose_name="توضیحات کامل",
    )

    client_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="نام مشتری",
    )

    website_url = models.URLField(
        blank=True,
        verbose_name="آدرس سایت",
    )

    technologies = models.JSONField(
        default=list,
        blank=True,
        verbose_name="تکنولوژی‌ها",
    )

    cover_image = models.ImageField(
        upload_to=upload_portfolio_cover,
        blank=True,
        null=True,
        validators=[
            validate_portfolio_image,
        ],
        verbose_name="تصویر اصلی",
    )


    completed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تکمیل",
    )


    project_url = models.URLField(
        blank=True,
        verbose_name="لینک پروژه",
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="نمونه‌کار ویژه",
    )

    is_published = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="منتشر شده",
    )


    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد بازدید",
    )


    class Meta:

        verbose_name = "نمونه‌کار"

        verbose_name_plural = "نمونه‌کارها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_active",
                    "is_published",
                ]
            ),

            models.Index(
                fields=[
                    "is_featured",
                ]
            ),

        ]


    def get_absolute_url(self):

        return reverse(
            "portfolio_detail",
            kwargs={
                "slug": self.slug
            }
        )


    def increase_views(self):

        self.views_count += 1

        self.save(
            update_fields=[
                "views_count",
            ]
        )


    def __str__(self):

        return self.title

# ==========================================================
# PORTFOLIO IMAGE MODEL
# ==========================================================

class PortfolioImage(UUIDModel):

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="نمونه‌کار",
    )

    image = models.ImageField(
        upload_to=upload_portfolio_gallery,
        validators=[
            validate_portfolio_image,
        ],
        verbose_name="تصویر",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="عنوان تصویر",
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="متن جایگزین تصویر",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات تصویر",
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتیب نمایش",
    )


    is_featured = models.BooleanField(
        default=False,
        verbose_name="تصویر اصلی گالری",
    )

    class Meta:
        verbose_name = "تصویر نمونه‌کار"
        verbose_name_plural = "تصاویر نمونه‌کار"
        ordering = [
            "order",
            "-created_at",
        ]
        indexes = [

            models.Index(
                fields=[
                    "portfolio",
                    "order",
                ]
            ),
        ]

    def __str__(self):
        if self.title:
            return self.title
        return self.portfolio.title

# ==========================================================
# ORDER MODEL
# ==========================================================

class Order(UUIDModel):

    STATUS_CHOICES = (

        ("pending", "در انتظار بررسی"),

        ("approved", "تایید شده"),

        ("planning", "برنامه‌ریزی"),

        ("development", "در حال توسعه"),

        ("review", "بازبینی مشتری"),

        ("completed", "تکمیل شده"),

        ("cancelled", "لغو شده"),
    )

    PRIORITY_CHOICES = (

        ("low", "کم"),

        ("normal", "عادی"),

        ("high", "زیاد"),

        ("urgent", "فوری"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کاربر",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="سرویس",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="نام مشتری",
    )

    phone = models.CharField(
        max_length=11,
        validators=[
            phone_validator,
        ],
        verbose_name="شماره موبایل",
    )

    attachment = models.FileField(
            upload_to="orders/attachments/",
            blank=True,
            null=True,
            verbose_name="فایل پیوست"
        )

    email = models.EmailField(
        blank=True,
        verbose_name="ایمیل",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان پروژه",
    )

    description = models.TextField(
        verbose_name="توضیحات سفارش",
    )

    estimated_price = models.PositiveBigIntegerField(
        default=0,
        verbose_name="هزینه تخمینی",
    )

    final_price = models.PositiveBigIntegerField(
        default=0,
        verbose_name="هزینه نهایی",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
        verbose_name="وضعیت",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        db_index=True,
        verbose_name="اولویت",
    )

    tracking_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        validators=[
            tracking_code_validator,
        ],
        verbose_name="کد پیگیری",
    )

    developers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="assigned_orders",
        verbose_name="توسعه‌دهندگان",
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="شروع پروژه",
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="اتمام پروژه",
    )


    class Meta:

        verbose_name = "سفارش"

        verbose_name_plural = "سفارش‌ها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "status",
                    "priority",
                ]
            ),

            models.Index(
                fields=[
                    "user",
                    "-created_at",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.tracking_code:

            self.tracking_code = generate_tracking_code()


        super().save(
            *args,
            **kwargs
        )


    def clean(self):

        if self.final_price and self.final_price < self.estimated_price:

            raise ValidationError(
                "هزینه نهایی نمی‌تواند کمتر از هزینه تخمینی باشد."
            )


    def __str__(self):

        return (
            f"{self.title} - "
            f"{self.tracking_code}"
        )

# ==========================================================
# ORDER FILE MODEL
# ==========================================================

class OrderFile(UUIDModel):

    FILE_TYPE_CHOICES = (

        ("document", "سند"),

        ("design", "طراحی"),

        ("source", "سورس"),

        ("image", "تصویر"),

        ("archive", "فایل فشرده"),

        ("other", "سایر"),

    )


    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="سفارش",
    )


    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_order_files",
        verbose_name="آپلود کننده",
    )


    file = models.FileField(
        upload_to=upload_order_file,
        validators=[
            validate_document,
        ],
        verbose_name="فایل",
    )


    title = models.CharField(
        max_length=200,
        verbose_name="عنوان فایل",
    )


    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default="other",
        db_index=True,
        verbose_name="نوع فایل",
    )


    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )


    size = models.PositiveBigIntegerField(
        default=0,
        editable=False,
        verbose_name="حجم فایل",
    )


    is_public = models.BooleanField(
        default=False,
        verbose_name="قابل نمایش برای مشتری",
    )


    class Meta:

        verbose_name = "فایل سفارش"

        verbose_name_plural = "فایل‌های سفارش"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "order",
                    "file_type",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        if self.file:

            self.size = self.file.size


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return self.title

# ==========================================================
# TICKET MODEL
# ==========================================================

class Ticket(UUIDModel):

    STATUS_CHOICES = (

        ("open", "باز"),

        ("pending", "در انتظار پاسخ"),

        ("answered", "پاسخ داده شده"),

        ("closed", "بسته شده"),

        ("resolved", "حل شده"),

    )


    PRIORITY_CHOICES = (

        ("low", "کم"),

        ("normal", "عادی"),

        ("high", "زیاد"),

        ("urgent", "فوری"),

    )


    CATEGORY_CHOICES = (

        ("technical", "فنی"),

        ("billing", "مالی"),

        ("support", "پشتیبانی"),

        ("project", "پروژه"),

        ("other", "سایر"),

    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="کاربر",
    )


    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
        verbose_name="سفارش مرتبط",
    )


    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        verbose_name="مسئول رسیدگی",
    )

    department = models.CharField(
        max_length=100,
        verbose_name="بخش مربوطه"
    )

    department = models.CharField(
        max_length=50,
        choices=[
            ("support", "پشتیبانی"),
            ("technical", "فنی"),
            ("billing", "مالی"),
            ("sales", "فروش"),
        ],
        default="support",
        verbose_name="بخش"
    )


    attachment = models.FileField(
        upload_to="tickets/attachments/",
        blank=True,
        null=True,
        verbose_name="فایل پیوست"
    )

    attachment = models.FileField(
        upload_to="tickets/",
        blank=True,
        null=True,
        verbose_name="فایل پیوست"
    )

    ticket_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        verbose_name="شماره تیکت",
    )


    subject = models.CharField(
        max_length=255,
        verbose_name="موضوع",
    )


    message = models.TextField(
        verbose_name="متن پیام",
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="دپارتمان"
    )


    attachment = models.FileField(
        upload_to="tickets/attachments/",
        blank=True,
        null=True,
        validators=[
            validate_document,
        ],
        verbose_name="فایل پیوست"
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="support",
        db_index=True,
        verbose_name="دسته‌بندی",
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        db_index=True,
        verbose_name="وضعیت",
    )


    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        db_index=True,
        verbose_name="اولویت",
    )


    last_reply_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="آخرین پاسخ",
    )


    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان بسته شدن",
    )


    class Meta:

        verbose_name = "تیکت"

        verbose_name_plural = "تیکت‌ها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "status",
                    "priority",
                ]
            ),

            models.Index(
                fields=[
                    "user",
                    "-created_at",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.ticket_number:

            self.ticket_number = generate_ticket_number()


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return (
            f"{self.ticket_number} - "
            f"{self.subject}"
        )

# ==========================================================
# TICKET REPLY MODEL
# ==========================================================

class TicketReply(UUIDModel):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name="تیکت",
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_replies",
        verbose_name="کاربر",
    )


    message = models.TextField(
        verbose_name="متن پاسخ",
    )


    is_staff_reply = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="پاسخ تیم",
    )


    is_internal = models.BooleanField(
        default=False,
        verbose_name="یادداشت داخلی",
    )


    class Meta:

        verbose_name = "پاسخ تیکت"

        verbose_name_plural = "پاسخ‌های تیکت"

        ordering = [
            "created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "ticket",
                    "created_at",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        self.ticket.last_reply_at = timezone.now()

        self.ticket.save(
            update_fields=[
                "last_reply_at",
            ]
        )


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return (
            f"Reply - "
            f"{self.ticket.ticket_number}"
        )



# ==========================================================
# TICKET ATTACHMENT MODEL
# ==========================================================

class TicketAttachment(UUIDModel):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="تیکت",
    )


    reply = models.ForeignKey(
        TicketReply,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
        verbose_name="پاسخ مرتبط",
    )


    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_attachments",
        verbose_name="آپلود کننده",
    )


    file = models.FileField(
        upload_to=upload_ticket_attachment,
        validators=[
            validate_document,
        ],
        verbose_name="فایل",
    )


    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="عنوان فایل",
    )


    class Meta:

        verbose_name = "فایل تیکت"

        verbose_name_plural = "فایل‌های تیکت"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "ticket",
                    "-created_at",
                ]
            ),

        ]


    def __str__(self):

        return (
            self.title
            or self.file.name
        )

# ==========================================================
# INVOICE MODEL
# ==========================================================

class Invoice(UUIDModel):

    STATUS_CHOICES = (

        ("draft", "پیش‌نویس"),

        ("issued", "صادر شده"),

        ("sent", "ارسال شده"),

        ("paid", "پرداخت شده"),

        ("cancelled", "لغو شده"),

    )


    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice",
        verbose_name="سفارش",
    )


    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        validators=[
            invoice_number_validator,
        ],
        verbose_name="شماره فاکتور",
    )

    pdf = models.FileField(
        upload_to="invoices/",
        blank=True,
        null=True,
        verbose_name="فایل PDF فاکتور"
    )

    title = models.CharField(
        max_length=255,
        default="Nexora Web Service Invoice",
        verbose_name="عنوان فاکتور",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )


    amount = models.PositiveBigIntegerField(
        default=0,
        verbose_name="مبلغ",
    )


    discount = models.PositiveBigIntegerField(
        default=0,
        verbose_name="تخفیف",
    )


    tax = models.PositiveBigIntegerField(
        default=0,
        verbose_name="مالیات",
    )


    final_amount = models.PositiveBigIntegerField(
        default=0,
        editable=False,
        verbose_name="مبلغ نهایی",
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True,
        verbose_name="وضعیت",
    )


    issued_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ صدور",
    )


    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="مهلت پرداخت",
    )


    class Meta:

        verbose_name = "فاکتور"

        verbose_name_plural = "فاکتورها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "status",
                    "-created_at",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.invoice_number:

            self.invoice_number = generate_invoice_number()


        self.final_amount = (
            self.amount
            - self.discount
            + self.tax
        )


        if not self.issued_at:

            self.issued_at = timezone.now()


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return self.invoice_number

# ==========================================================
# PAYMENT MODEL
# ==========================================================

class Payment(UUIDModel):

    STATUS_CHOICES = (

        ("pending", "در انتظار پرداخت"),

        ("processing", "در حال پردازش"),

        ("paid", "پرداخت موفق"),

        ("failed", "ناموفق"),

        ("cancelled", "لغو شده"),

        ("refunded", "بازگشت وجه"),

    )


    METHOD_CHOICES = (

        ("gateway", "درگاه پرداخت"),

        ("card", "کارت به کارت"),

        ("crypto", "ارز دیجیتال"),

        ("cash", "نقدی"),

        ("other", "سایر"),

    )


    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="سفارش",
    )

    gateway = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="درگاه پرداخت",
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="فاکتور",
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="کاربر",
    )


    amount = models.PositiveBigIntegerField(
        default=0,
        verbose_name="مبلغ پرداختی",
    )


    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name="شناسه تراکنش",
    )


    gateway_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام درگاه",
    )


    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default="gateway",
        verbose_name="روش پرداخت",
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
        verbose_name="وضعیت",
    )


    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان پرداخت",
    )


    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="اطلاعات اضافی",
    )


    class Meta:

        verbose_name = "پرداخت"

        verbose_name_plural = "پرداخت‌ها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "status",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "transaction_id",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        if self.status == "paid" and not self.paid_at:

            self.paid_at = timezone.now()


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return (
            f"{self.order.title} - "
            f"{self.amount}"
        )

# ==========================================================
# NOTIFICATION MODEL
# ==========================================================

class Notification(UUIDModel):

    TYPE_CHOICES = (

        ("order", "سفارش"),

        ("payment", "پرداخت"),

        ("ticket", "تیکت"),

        ("project", "پروژه"),

        ("security", "امنیتی"),

        ("system", "سیستم"),

    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="کاربر",
    )


    title = models.CharField(
        max_length=255,
        verbose_name="عنوان",
    )


    message = models.TextField(
        verbose_name="متن اعلان",
    )


    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="system",
        db_index=True,
        verbose_name="نوع اعلان",
    )


    related_url = models.URLField(
        blank=True,
        verbose_name="لینک مرتبط",
    )


    is_read = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="خوانده شده",
    )


    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان خواندن",
    )


    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="اطلاعات اضافی",
    )


    class Meta:

        verbose_name = "اعلان"

        verbose_name_plural = "اعلان‌ها"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "user",
                    "is_read",
                ]
            ),

            models.Index(
                fields=[
                    "notification_type",
                    "-created_at",
                ]
            ),

        ]


    def mark_as_read(self):

        if not self.is_read:

            self.is_read = True

            self.read_at = timezone.now()

            self.save(
                update_fields=[
                    "is_read",
                    "read_at",
                ]
            )


    def __str__(self):

        return self.title
    
# ==========================================================
# CONTACT MESSAGE MODEL
# ==========================================================

class ContactMessage(UUIDModel):

    STATUS_CHOICES = (

        ("new", "جدید"),

        ("read", "خوانده شده"),

        ("in_progress", "در حال بررسی"),

        ("answered", "پاسخ داده شده"),

        ("closed", "بسته شده"),

    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_messages",
        verbose_name="کاربر",
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="خوانده شده"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="نام",
    )

    email = models.EmailField(
        verbose_name="ایمیل",
    )

    phone = models.CharField(
        max_length=11,
        blank=True,
        validators=[
            phone_validator,
        ],
        verbose_name="شماره موبایل",
    )

    subject = models.CharField(
        max_length=255,
        verbose_name="موضوع",
    )

    message = models.TextField(
        verbose_name="پیام",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        db_index=True,
        verbose_name="وضعیت",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_contact_messages",
        verbose_name="مسئول بررسی",
    )

    answered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان پاسخ",
    )


    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="آدرس IP",
    )


    user_agent = models.TextField(
        blank=True,
        verbose_name="اطلاعات مرورگر",
    )


    class Meta:

        verbose_name = "پیام تماس"

        verbose_name_plural = "پیام‌های تماس"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "status",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "email",
                ]
            ),

        ]


    def mark_as_answered(self):

        self.status = "answered"

        self.answered_at = timezone.now()

        self.save(
            update_fields=[
                "status",
                "answered_at",
            ]
        )


    def __str__(self):

        return (
            f"{self.name} - "
            f"{self.subject}"
        )

# ==========================================================
# SITE SETTING MODEL
# ==========================================================

class SiteSetting(UUIDModel):

    site_name = models.CharField(
        max_length=200,
        default="Nexora Web",
        verbose_name="نام سایت",
    )


    site_title = models.CharField(
        max_length=255,
        default="Nexora Web - Web Development",
        verbose_name="عنوان مرورگر",
    )


    logo = models.ImageField(
        upload_to="site/logo/",
        blank=True,
        null=True,
        verbose_name="لوگو",
    )


    favicon = models.ImageField(
        upload_to="site/favicon/",
        blank=True,
        null=True,
        verbose_name="فاوآیکون",
    )


    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="تلفن",
    )


    email = models.EmailField(
        blank=True,
        verbose_name="ایمیل",
    )


    address = models.TextField(
        blank=True,
        verbose_name="آدرس",
    )


    short_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="توضیح کوتاه سایت",
    )


    about = models.TextField(
        blank=True,
        verbose_name="درباره ما",
    )


    instagram = models.URLField(
        blank=True,
        verbose_name="اینستاگرام",
    )


    telegram = models.URLField(
        blank=True,
        verbose_name="تلگرام",
    )


    linkedin = models.URLField(
        blank=True,
        verbose_name="لینکدین",
    )


    github = models.URLField(
        blank=True,
        verbose_name="گیت‌هاب",
    )


    youtube = models.URLField(
        blank=True,
        verbose_name="یوتیوب",
    )


    meta_description = models.TextField(
        blank=True,
        verbose_name="توضیحات متا SEO",
    )


    meta_keywords = models.TextField(
        blank=True,
        verbose_name="کلمات کلیدی SEO",
    )


    google_analytics_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Google Analytics ID",
    )


    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name="حالت تعمیرات",
    )


    class Meta:

        verbose_name = "تنظیمات سایت"

        verbose_name_plural = "تنظیمات سایت"


    def save(
        self,
        *args,
        **kwargs
    ):

        if SiteSetting.objects.exists() and not self.pk:

            raise ValidationError(
                "فقط یک تنظیمات سایت مجاز است."
            )


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return self.site_name

# ==========================================================
# FAQ MODEL
# ==========================================================

class FAQ(UUIDModel):

    question = models.CharField(
        max_length=300,
        verbose_name="سوال",
    )


    answer = models.TextField(
        verbose_name="پاسخ",
    )


    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="دسته‌بندی",
    )


    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتیب نمایش",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="نمایش ویژه",
    )


    class Meta:

        verbose_name = "سوال متداول"

        verbose_name_plural = "سوالات متداول"

        ordering = [
            "order",
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_featured",
                    "order",
                ]
            ),

        ]


    def __str__(self):

        return self.question

# ==========================================================
# TEAM MODEL
# ==========================================================

class Team(UUIDModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_profile",
        verbose_name="کاربر",
    )


    position = models.CharField(
        max_length=200,
        verbose_name="سمت",
    )


    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
    )


    avatar = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True,
        verbose_name="تصویر پروفایل",
    )

    name = models.CharField(
            max_length=100,
            verbose_name="نام"
        )

    role = models.CharField(
        max_length=100,
        verbose_name="سمت"
    )

    skills = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="مهارت‌ها",
    )


    linkedin = models.URLField(
        blank=True,
        verbose_name="لینکدین",
    )


    github = models.URLField(
        blank=True,
        verbose_name="گیت‌هاب",
    )


    website = models.URLField(
        blank=True,
        verbose_name="وب‌سایت شخصی",
    )


    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتیب نمایش",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="عضو ویژه",
    )


    class Meta:

        verbose_name = "عضو تیم"

        verbose_name_plural = "اعضای تیم"

        ordering = [
            "order",
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_featured",
                    "order",
                ]
            ),

        ]


    def __str__(self):

        return (
            self.user.get_full_name()
            or self.user.username
        )

# ==========================================================
# REVIEW MODEL
# ==========================================================

class Review(UUIDModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
        verbose_name="کاربر",
    )


    name = models.CharField(
        max_length=100,
        verbose_name="نام مشتری",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="عنوان نظر"
    )


    comment = models.TextField(
        verbose_name="متن نظر",
    )

    company = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="شرکت",
    )


    avatar = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True,
        verbose_name="تصویر مشتری",
    )


    message = models.TextField(
        verbose_name="متن نظر",
    )


    rating = models.PositiveIntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="امتیاز",
    )


    project = models.ForeignKey(
        Portfolio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
        verbose_name="پروژه مرتبط",
    )


    is_verified = models.BooleanField(
        default=False,
        verbose_name="تایید شده",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="نمایش ویژه",
    )


    class Meta:

        verbose_name = "نظر مشتری"

        verbose_name_plural = "نظرات مشتریان"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_featured",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "rating",
                    "message",
                    "rating",
                ]
            ),

        ]


    def __str__(self):

        return self.name

# ==========================================================
# BLOG CATEGORY MODEL
# ==========================================================

class BlogCategory(SlugModel):

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )


    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="آیکون FontAwesome",
    )


    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتیب نمایش",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="دسته‌بندی ویژه",
    )


    class Meta:

        verbose_name = "دسته‌بندی مقاله"

        verbose_name_plural = "دسته‌بندی‌های مقاله"

        ordering = [
            "order",
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_featured",
                    "order",
                ]
            ),

        ]


    def __str__(self):

        return self.title

# ==========================================================
# TAG MODEL
# ==========================================================

class Tag(UUIDModel):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام تگ",
    )


    slug = models.SlugField(
        unique=True,
        max_length=100,
        validators=[
            english_slug_validator,
        ],
        verbose_name="اسلاگ",
    )


    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )


    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتیب نمایش",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="تگ ویژه",
    )


    class Meta:

        verbose_name = "تگ"

        verbose_name_plural = "تگ‌ها"

        ordering = [
            "order",
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_featured",
                    "order",
                ]
            ),

        ]


    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.slug:

            self.slug = slugify(
                self.name
            )


        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return self.name

# ==========================================================
# BLOG MODEL
# ==========================================================

class Blog(SlugModel):

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
        verbose_name="دسته‌بندی",
    )


    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="blogs",
        verbose_name="تگ‌ها",
    )


    short_description = models.CharField(
        max_length=300,
        verbose_name="توضیح کوتاه",
    )


    content = models.TextField(
        verbose_name="محتوا",
    )


    image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="تصویر مقاله",
    )


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
        verbose_name="نویسنده",
    )


    views = models.PositiveIntegerField(
        default=0,
        verbose_name="بازدید",
    )


    reading_time = models.PositiveIntegerField(
        default=5,
        verbose_name="زمان مطالعه (دقیقه)",
    )


    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="مقاله ویژه",
    )


    is_published = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="منتشر شده",
    )


    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ انتشار",
    )


    meta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="عنوان SEO",
    )


    meta_description = models.TextField(
        blank=True,
        verbose_name="توضیحات SEO",
    )


    class Meta:

        verbose_name = "مقاله"

        verbose_name_plural = "مقالات"

        ordering = [
            "-created_at",
        ]


        indexes = [

            models.Index(
                fields=[
                    "is_published",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "is_featured",
                ]
            ),

        ]


    def get_absolute_url(self):

        return reverse(
            "blog_detail",
            kwargs={
                "slug": self.slug
            }
        )


    def __str__(self):

        return self.title

# ==========================================================
# JOB APPLICATION MODEL
# ==========================================================

class JobApplication(UUIDModel):

    STATUS_CHOICES = [
        ("pending", "در انتظار بررسی"),
        ("accepted", "پذیرفته شده"),
        ("rejected", "رد شده"),
    ]

    full_name = models.CharField(
        max_length=150,
        verbose_name="نام کامل"
    )

    email = models.EmailField(
        verbose_name="ایمیل"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تماس"
    )

    position = models.CharField(
        max_length=150,
        verbose_name="موقعیت شغلی"
    )

    skills = models.TextField(
        blank=True,
        verbose_name="مهارت‌ها"
    )

    portfolio = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک نمونه کار"
    )

    experience = models.TextField(
        blank=True,
        verbose_name="تجربه کاری"
    )

    resume = models.FileField(
        upload_to="applications/resumes/",
        blank=True,
        null=True,
        verbose_name="رزومه"
    )

    message = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )


    class Meta:
        verbose_name = "درخواست همکاری"
        verbose_name_plural = "درخواست‌های همکاری"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.full_name} - {self.position}"

class ProjectStatus(models.TextChoices):

    PLANNING = "planning", "برنامه‌ریزی"

    DEVELOPMENT = "development", "در حال توسعه"

    TESTING = "testing", "در حال تست"

    DEPLOYMENT = "deployment", "آماده انتشار"

    COMPLETED = "completed", "تکمیل شده"

class ProjectTask(models.Model):
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان وظیفه"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_tasks",
        verbose_name="مسئول انجام"
    )

    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name="مهلت انجام"
    )

    def __str__(self):
        return self.title

class SupportTicket(UUIDModel):
    STATUS_CHOICES = (
        ("open", "باز"),
        ("pending", "در انتظار پاسخ"),
        ("answered", "پاسخ داده شده"),
        ("closed", "بسته شده"),
    )

    PRIORITY_CHOICES = (
        ("low", "کم"),
        ("normal", "عادی"),
        ("high", "زیاد"),
        ("urgent", "فوری"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="support_tickets",
        verbose_name="کاربر",
    )

    subject = models.CharField(
        max_length=255,
        verbose_name="موضوع",
    )

    message = models.TextField(
        verbose_name="متن پیام",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        db_index=True,
        verbose_name="وضعیت",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        db_index=True,
        verbose_name="اولویت",
    )

    admin_reply = models.TextField(
        blank=True,
        null=True,
        verbose_name="پاسخ مدیریت",
    )

    attachment = models.FileField(
        upload_to="support/tickets/",
        blank=True,
        null=True,
        verbose_name="فایل پیوست",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی",
    )

    closed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="زمان بسته شدن",
    )


    class Meta:
        verbose_name = "تیکت پشتیبانی"
        verbose_name_plural = "تیکت‌های پشتیبانی"
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["user", "status"]
            ),
            models.Index(
                fields=["priority", "-created_at"]
            ),
        ]

    def __str__(self):
        return f"{self.subject} - {self.user}"

class Project(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("planning", "برنامه‌ریزی"),
        ("development", "در حال توسعه"),
        ("testing", "تست"),
        ("completed", "تکمیل شده"),
        ("cancelled", "لغو شده"),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان پروژه"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="اسلاگ"
    )

    description = models.TextField(
        verbose_name="توضیحات پروژه"
    )

    client_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="نام مشتری"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت"
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ شروع"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
        verbose_name="تصویر پروژه"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class VersionHistory(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    version = models.CharField(
        max_length=50,
        verbose_name="نسخه"
    )

    changes = models.TextField(
        verbose_name="تغییرات"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "تاریخچه نسخه"
        verbose_name_plural = "تاریخچه نسخه‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project} - {self.version}"
    
class Contract(models.Model):
    STATUS_CHOICES = [
        ("draft", "پیش‌نویس"),
        ("active", "فعال"),
        ("completed", "تکمیل شده"),
        ("cancelled", "لغو شده"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contracts",
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان قرارداد"
    )

    client_name = models.CharField(
        max_length=200,
        verbose_name="نام مشتری"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ قرارداد"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="وضعیت"
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "قرارداد"
        verbose_name_plural = "قراردادها"

    def __str__(self):
        return self.title

from django.conf import settings
from django.db import models


class Report(models.Model):
    REPORT_TYPES = (
        ("project", "گزارش پروژه"),
        ("financial", "گزارش مالی"),
        ("technical", "گزارش فنی"),
        ("progress", "گزارش پیشرفت"),
        ("system", "گزارش سیستم"),
        ("other", "سایر"),
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    description = models.TextField(
        verbose_name="توضیحات"
    )

    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPES,
        default="project",
        verbose_name="نوع گزارش"
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="reports",
        null=True,
        blank=True,
        verbose_name="پروژه"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
        verbose_name="ایجادکننده"
    )

    file = models.FileField(
        upload_to="reports/",
        null=True,
        blank=True,
        verbose_name="فایل گزارش"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "گزارش"
        verbose_name_plural = "گزارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class CompanySetting(models.Model):

    name = models.CharField(
        max_length=255,
        default="Nexora",
        verbose_name="نام شرکت"
    )

    logo = models.ImageField(
        upload_to="company/",
        blank=True,
        null=True,
        verbose_name="لوگو"
    )

    company_name = models.CharField(
        max_length=255,
        default="Nexora",
        verbose_name="نام شرکت"
    )


    favicon = models.ImageField(
        upload_to="company/favicon/",
        blank=True,
        null=True,
        verbose_name="فاوآیکون"
    )

    about = models.TextField(
        blank=True,
        verbose_name="درباره شرکت"
    )

    address = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="آدرس"
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="تلفن"
    )

    email = models.EmailField(
        blank=True,
        verbose_name="ایمیل"
    )

    website = models.URLField(
        blank=True,
        verbose_name="وب‌سایت"
    )

    instagram = models.URLField(
        blank=True,
        verbose_name="اینستاگرام"
    )

    linkedin = models.URLField(
        blank=True,
        verbose_name="لینکدین"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        verbose_name = "تنظیمات شرکت"
        verbose_name_plural = "تنظیمات شرکت"


    def __str__(self):
        return self.name

class ProjectProgress(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="progresses"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان مرحله"
    )
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )
    progress = models.PositiveIntegerField(
        default=0,
        verbose_name="درصد پیشرفت"
    )
    percentage = models.PositiveIntegerField(
        default=0,
        verbose_name="درصد پیشرفت"
    )
    note = models.TextField(
        blank=True,
        verbose_name="یادداشت"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "پیشرفت پروژه"
        verbose_name_plural = "پیشرفت‌های پروژه"

    def clean(self):
        if self.percentage > 100:
            raise ValidationError(
                "درصد پیشرفت نمی‌تواند بیشتر از ۱۰۰ باشد."
            )
    def __str__(self):
        return f"{self.title} - {self.progress}%"

# ==========================================================
# PROJECT TIMELINE
# ==========================================================

class Timeline(BaseModel):

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان"
    )

    description = models.TextField(
        verbose_name="توضیحات"
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ شروع"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان"
    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="timeline_events",

    )

    title = models.CharField(

        max_length=200,

    )

    description = models.TextField(

        blank=True,

    )

    status = models.CharField(

        max_length=30,

        choices=ProjectStatus.choices,

        default=ProjectStatus.PLANNING,

        db_index=True,

    )

    event_date = models.DateTimeField(

        default=timezone.now,

        db_index=True,

    )

    class Meta:

        verbose_name = "رویداد پروژه"

        verbose_name_plural = "رویدادهای پروژه"

        ordering = [

            "-event_date",

        ]

        indexes = [

            models.Index(fields=["status"]),

            models.Index(fields=["event_date"]),

        ]

    def __str__(self):

        return self.title

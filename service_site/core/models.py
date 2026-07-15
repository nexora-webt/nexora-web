from uuid import uuid4
from pathlib import Path

from django.db import models
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver


# ==========================================================
# CONSTANTS
# ==========================================================

MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB


# ==========================================================
# HELPERS
# ==========================================================

def upload_to_portfolio(instance, filename):

    ext = Path(filename).suffix

    return (
        f"portfolio/"
        f"{uuid4().hex}"
        f"{ext}"
    )


def upload_to_orders(instance, filename):

    ext = Path(filename).suffix

    return (
        f"orders/"
        f"{instance.tracking_code}/"
        f"{uuid4().hex}"
        f"{ext}"
    )


def upload_to_versions(instance, filename):

    ext = Path(filename).suffix

    return (
        f"versions/"
        f"{instance.order.tracking_code}/"
        f"v{instance.version}"
        f"{ext}"
    )


def upload_to_resumes(instance, filename):

    ext = Path(filename).suffix

    return (
        f"careers/"
        f"{uuid4().hex}"
        f"{ext}"
    )


def upload_to_tickets(instance, filename):

    ext = Path(filename).suffix

    return (
        f"tickets/"
        f"{instance.order.tracking_code}/"
        f"{uuid4().hex}"
        f"{ext}"
    )


# ==========================================================
# FILE VALIDATOR
# ==========================================================

def validate_file_size(file):

    if file.size > MAX_UPLOAD_SIZE:

        raise ValueError(
            "Maximum file size is 20MB."
        )


# ==========================================================
# ORDER STATUS
# ==========================================================

class OrderStatus(models.TextChoices):

    PENDING = "pending", "در انتظار"

    PROCESSING = "processing", "در حال انجام"

    REVIEW = "review", "در انتظار تایید"

    COMPLETED = "completed", "تکمیل شده"

    CANCELLED = "cancelled", "لغو شده"


# ==========================================================
# TASK STATUS
# ==========================================================

class TaskStatus(models.TextChoices):

    TODO = "todo", "انجام نشده"

    DOING = "doing", "در حال انجام"

    DONE = "done", "انجام شده"


# ==========================================================
# INVOICE STATUS
# ==========================================================

class InvoiceStatus(models.TextChoices):

    UNPAID = "unpaid", "پرداخت نشده"

    PAID = "paid", "پرداخت شده"

    CANCELLED = "cancelled", "باطل شده"

# ==========================================================
# SERVICE MODEL
# ==========================================================

class Service(models.Model):

    title = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name="عنوان سرویس",
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        allow_unicode=True,
        db_index=True,
        verbose_name="اسلاگ",
    )

    short_description = models.CharField(
        max_length=250,
        verbose_name="توضیح کوتاه",
    )

    description = models.TextField(
        verbose_name="توضیح کامل",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="آیکون FontAwesome",
        help_text="مثال: fas fa-code",
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
        verbose_name="تصویر سرویس",
    )

    base_price = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="قیمت پایه",
    )

    estimated_days = models.PositiveSmallIntegerField(
        default=7,
        verbose_name="مدت تقریبی اجرا (روز)",
    )

    featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="سرویس ویژه",
    )

    active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="فعال",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
    )

    seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="SEO Title",
    )

    seo_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="SEO Description",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی",
    )

    class Meta:

        verbose_name = "سرویس"

        verbose_name_plural = "سرویس‌ها"

        ordering = ["sort_order", "title"]

        indexes = [
            models.Index(fields=["active"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(
                self.title,
                allow_unicode=True,
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse(
            "service_detail",
            kwargs={
                "slug": self.slug,
            },
        )

# ==========================================================
# PORTFOLIO MODEL
# ==========================================================

class Portfolio(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="portfolios",
        verbose_name="سرویس",
    )

    title = models.CharField(
        max_length=180,
        db_index=True,
        verbose_name="عنوان پروژه",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        db_index=True,
        verbose_name="اسلاگ",
    )

    client = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="نام مشتری",
    )

    short_description = models.CharField(
        max_length=250,
        verbose_name="توضیح کوتاه",
    )

    description = models.TextField(
        verbose_name="توضیح کامل",
    )

    image = models.ImageField(
        upload_to=upload_to_portfolio,
        verbose_name="تصویر اصلی",
    )

    gallery_image = models.ImageField(
        upload_to=upload_to_portfolio,
        blank=True,
        null=True,
        verbose_name="تصویر دوم",
    )

    technologies = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="تکنولوژی‌ها",
        help_text="Python, Django, React, Bootstrap ...",
    )

    project_url = models.URLField(
        blank=True,
        verbose_name="آدرس پروژه",
    )

    github_url = models.URLField(
        blank=True,
        verbose_name="لینک GitHub",
    )

    featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="پروژه ویژه",
    )

    active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="فعال",
    )

    views = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد بازدید",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
    )

    seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="SEO Title",
    )

    seo_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="SEO Description",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی",
    )

    class Meta:

        verbose_name = "نمونه کار"

        verbose_name_plural = "نمونه کارها"

        ordering = ["sort_order", "-created_at"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(
                self.title,
                allow_unicode=True,
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse(

            "portfolio_detail",

            kwargs={

                "slug": self.slug,

            },

        )

# ==========================================================
# ORDER MODEL
# ==========================================================

class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="کاربر",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="سرویس",
    )

    tracking_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        editable=False,
        verbose_name="کد رهگیری",
    )

    website = models.URLField(
    blank=True,
    verbose_name="وب سایت",
    )

    telegram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="تلگرام",
    )

    budget = models.PositiveBigIntegerField(
        default=0,
        verbose_name="بودجه",
    )

    deadline = models.DateField(
        blank=True,
        null=True,
        verbose_name="ددلاین",
    )

    full_name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name="نام کامل",
    )

    email = models.EmailField(
        verbose_name="ایمیل",
    )

    phone = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="شماره تماس",
    )

    company = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="نام شرکت",
    )

    description = models.TextField(
        verbose_name="توضیحات پروژه",
    )

    attachment = models.FileField(
        upload_to=upload_to_orders,
        blank=True,
        null=True,
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "zip",
                    "rar",
                    "png",
                    "jpg",
                    "jpeg",
                    "fig",
                    "xd",
                    "psd",
                ]
            )
        ],
        verbose_name="فایل پیوست",
    )

    estimated_price = models.PositiveIntegerField(
        default=0,
        verbose_name="هزینه تقریبی",
    )

    final_price = models.PositiveIntegerField(
        default=0,
        verbose_name="هزینه نهایی",
    )

    estimated_days = models.PositiveSmallIntegerField(
        default=7,
        verbose_name="زمان تقریبی اجرا",
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
        verbose_name="وضعیت",
    )

    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name="درصد پیشرفت",
    )

    client_seen = models.BooleanField(
        default=False,
        verbose_name="مشاهده توسط مشتری",
    )

    admin_note = models.TextField(
        blank=True,
        verbose_name="یادداشت مدیریت",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="تاریخ ثبت",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی",
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاریخ تکمیل",
    )

    class Meta:

        verbose_name = "سفارش"

        verbose_name_plural = "سفارش‌ها"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["tracking_code"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["user"]),
        ]

    @property
    def remaining_days(self):

        if not self.deadline:
            return None

        return (self.deadline - timezone.now().date()).days

    def __str__(self):

        return f"{self.tracking_code} - {self.full_name}"

    def save(self, *args, **kwargs):

        if not self.tracking_code:

            self.tracking_code = uuid4().hex[:10].upper()

        if (
            self.status == OrderStatus.COMPLETED
            and self.completed_at is None
        ):
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse(
            "order_detail",
            kwargs={
                "tracking_code": self.tracking_code,
            },
        )

# ==========================================================
# CAREER MODEL
# ==========================================================

class Career(models.Model):

    title = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name="عنوان شغل",
    )

    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        db_index=True,
    )

    short_description = models.CharField(
        max_length=250,
        verbose_name="توضیح کوتاه",
    )

    description = models.TextField(
        verbose_name="شرح کامل",
    )

    requirements = models.TextField(
        blank=True,
        verbose_name="شرایط استخدام",
    )

    responsibilities = models.TextField(
        blank=True,
        verbose_name="وظایف",
    )

    benefits = models.TextField(
        blank=True,
        verbose_name="مزایا",
    )

    salary = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="حقوق",
    )

    location = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="محل کار",
    )

    work_type = models.CharField(
        max_length=80,
        default="Remote",
        verbose_name="نوع همکاری",
    )

    experience = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="سابقه مورد نیاز",
    )

    vacancies = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد ظرفیت",
    )

    active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="فعال",
    )

    featured = models.BooleanField(
        default=False,
        verbose_name="ویژه",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [

            "sort_order",

            "-created_at",

        ]

        verbose_name = "فرصت شغلی"

        verbose_name_plural = "فرصت‌های شغلی"

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(

                self.title,

                allow_unicode=True,

            )

        super().save(*args, **kwargs)


# ==========================================================
# JOB APPLICATION MODEL
# ==========================================================

class JobApplication(models.Model):

    career = models.ForeignKey(

        Career,

        on_delete=models.CASCADE,

        related_name="applications",

    )

    full_name = models.CharField(

        max_length=150,

        db_index=True,

    )

    email = models.EmailField()

    phone = models.CharField(

        max_length=20,

    )

    city = models.CharField(

        max_length=100,

        blank=True,

    )

    age = models.PositiveSmallIntegerField(

        blank=True,

        null=True,

    )

    experience = models.CharField(

        max_length=150,

        blank=True,

    )

    github = models.URLField(

        blank=True,

    )

    linkedin = models.URLField(

        blank=True,

    )

    portfolio = models.URLField(

        blank=True,

    )

    website = models.URLField(

        blank=True,

    )

    resume = models.FileField(

        upload_to=upload_to_resumes,

        validators=[

            validate_file_size,

            FileExtensionValidator(

                [

                    "pdf",

                    "doc",

                    "docx",

                ]

            ),

        ],

    )

    cover_letter = models.TextField(

        blank=True,

    )

    reviewed = models.BooleanField(

        default=False,

    )

    accepted = models.BooleanField(

        default=False,

    )

    rejected = models.BooleanField(

        default=False,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = [

            "-created_at",

        ]

        verbose_name = "درخواست همکاری"

        verbose_name_plural = "درخواست‌های همکاری"

    def __str__(self):

        return f"{self.full_name} - {self.career}"

# ==========================================================
# DEPARTMENT
# ==========================================================

class Department(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name="نام دپارتمان",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "دپارتمان"
        verbose_name_plural = "دپارتمان‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ==========================================================
# EMPLOYEE
# ==========================================================

class Employee(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="core_employee",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    position = models.CharField(
        max_length=150,
    )

    salary = models.PositiveIntegerField(
        default=0,
    )

    hire_date = models.DateField()

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"

    def __str__(self):
        return f"{self.user.username} - {self.position}"


# ==========================================================
# USER PROFILE
# ==========================================================

class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="core_profile",
    )

    avatar = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    birthday = models.DateField(
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    github = models.URLField(
        blank=True,
    )

    linkedin = models.URLField(
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"

    def __str__(self):
        return self.user.username

# ==========================================================
# INVOICE
# ==========================================================

class Invoice(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="invoice",
        verbose_name="سفارش",
    )

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        verbose_name="شماره فاکتور",
    )

    amount = models.PositiveIntegerField(
        default=0,
        verbose_name="مبلغ",
    )

    tax = models.PositiveIntegerField(
        default=0,
        verbose_name="مالیات",
    )

    discount = models.PositiveIntegerField(
        default=0,
        verbose_name="تخفیف",
    )

    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.UNPAID,
        db_index=True,
        verbose_name="وضعیت",
    )

    due_date = models.DateField(
        verbose_name="تاریخ سررسید",
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاریخ پرداخت",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "فاکتور"

        verbose_name_plural = "فاکتورها"

        ordering = [
            "-created_at",
        ]

    def save(self, *args, **kwargs):

        if not self.invoice_number:

            self.invoice_number = (
                f"INV-{timezone.now().strftime('%Y%m%d')}-{uuid4().hex[:6].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.invoice_number

# ==========================================================
# PAYMENT
# ==========================================================

class Payment(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.PositiveIntegerField()

    authority = models.CharField(
        max_length=120,
        blank=True,
    )

    ref_id = models.CharField(
        max_length=120,
        blank=True,
    )

    gateway = models.CharField(
        max_length=50,
        default="Zarinpal",
    )

    successful = models.BooleanField(
        default=False,
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.invoice.invoice_number}"


# ==========================================================
# CONTRACT
# ==========================================================

class Contract(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="contract",
    )

    title = models.CharField(
        max_length=200,
    )

    file = models.FileField(
        upload_to="contracts/",
        blank=True,
        null=True,
    )

    signed_by_client = models.BooleanField(
        default=False,
    )

    signed_by_company = models.BooleanField(
        default=False,
    )

    signed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    expires_at = models.DateField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "قرارداد"
        verbose_name_plural = "قراردادها"

    def __str__(self):

        return self.title

# ==========================================================
# TEAM
# ==========================================================

class Team(models.Model):

    full_name = models.CharField(
        max_length=150,
    )

    position = models.CharField(
        max_length=150,
    )

    image = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
    )

    github = models.URLField(
        blank=True,
    )

    linkedin = models.URLField(
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"

        ordering = [
            "sort_order",
        ]

    def __str__(self):

        return self.full_name


# ==========================================================
# PARTNER
# ==========================================================

class Partner(models.Model):

    name = models.CharField(
        max_length=150,
    )

    logo = models.ImageField(
        upload_to="partners/",
    )

    website = models.URLField(
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "همکار"
        verbose_name_plural = "همکاران"

    def __str__(self):

        return self.name


# ==========================================================
# FAQ
# ==========================================================

class FAQ(models.Model):

    question = models.CharField(
        max_length=300,
    )

    answer = models.TextField()

    active = models.BooleanField(
        default=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"

        ordering = [
            "sort_order",
        ]

    def __str__(self):

        return self.question

# ==========================================================
# API KEY
# ==========================================================

class APIKey(models.Model):

    name = models.CharField(
        max_length=150,
    )

    key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:

        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self):
        return self.name


# ==========================================================
# ACTIVITY LOG
# ==========================================================

class ActivityLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=200,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "لاگ فعالیت"
        verbose_name_plural = "لاگ فعالیت‌ها"

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.action


# ==========================================================
# LOGIN HISTORY
# ==========================================================

class LoginHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_history",
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField(
        blank=True,
    )

    successful = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "تاریخچه ورود"
        verbose_name_plural = "تاریخچه ورود"

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return str(self.user)


# ==========================================================
# SITE SETTINGS
# ==========================================================

class SiteSetting(models.Model):

    site_name = models.CharField(
        max_length=150,
    )

    logo = models.ImageField(
        upload_to="settings/",
        blank=True,
        null=True,
    )

    favicon = models.ImageField(
        upload_to="settings/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    telegram = models.URLField(
        blank=True,
    )

    instagram = models.URLField(
        blank=True,
    )

    github = models.URLField(
        blank=True,
    )

    linkedin = models.URLField(
        blank=True,
    )

    maintenance_mode = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name

# ==========================================================
# CONTACT MODEL
# ==========================================================

class Contact(models.Model):

    full_name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name="نام کامل",
    )

    email = models.EmailField(
        verbose_name="ایمیل",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تماس",
    )

    company = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="شرکت",
    )

    subject = models.CharField(
        max_length=200,
        verbose_name="موضوع",
    )

    message = models.TextField(
        verbose_name="پیام",
    )

    is_read = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="خوانده شده",
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="IP",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت",
    )

    class Meta:

        verbose_name = "پیام تماس"

        verbose_name_plural = "پیام‌های تماس"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_read"]),
        ]

    def __str__(self):

        return self.full_name


# ==========================================================
# TICKET MODEL
# ==========================================================

class Ticket(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="سفارش",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="ارسال کننده",
    )

    message = models.TextField(
        verbose_name="پیام",
    )

    attachment = models.FileField(
        upload_to=upload_to_tickets,
        blank=True,
        null=True,
        validators=[
            validate_file_size,
            FileExtensionValidator(
                [
                    "pdf",
                    "zip",
                    "rar",
                    "png",
                    "jpg",
                    "jpeg",
                    "doc",
                    "docx",
                ]
            ),
        ],
        verbose_name="فایل پیوست",
    )

    is_admin = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="پیام مدیریت",
    )

    is_read = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="خوانده شده",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال",
    )

    class Meta:

        verbose_name = "تیکت"

        verbose_name_plural = "تیکت‌ها"

        ordering = ["created_at"]

        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["is_admin"]),
        ]

    def __str__(self):

        return f"{self.order.tracking_code} - {self.sender}"

# ==========================================================
# PROJECT PROGRESS
# ==========================================================

class ProjectProgress(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="progresses",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    completed = models.BooleanField(
        default=False,
    )

    is_visible_to_client = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "پیشرفت پروژه"

        verbose_name_plural = "پیشرفت پروژه"

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return f"{self.order.tracking_code} - {self.title}"


# ==========================================================
# PROJECT TIMELINE
# ==========================================================

class ProjectTimeline(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="timeline",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    event_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "تایم لاین"

        verbose_name_plural = "تایم لاین پروژه"

        ordering = [
            "event_date",
        ]

    def __str__(self):

        return self.title


# ==========================================================
# PROJECT TASK
# ==========================================================

class ProjectTask(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )

    deadline = models.DateField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "وظیفه"

        verbose_name_plural = "وظایف پروژه"

        ordering = [
            "deadline",
            "-created_at",
        ]

    def __str__(self):

        return self.title


# ==========================================================
# PROJECT VERSION
# ==========================================================

class ProjectVersion(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="versions",
    )

    version = models.CharField(
        max_length=30,
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    file = models.FileField(
        upload_to=upload_to_versions,
        validators=[
            validate_file_size,
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "نسخه پروژه"

        verbose_name_plural = "نسخه‌های پروژه"

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return f"{self.order.tracking_code} - {self.version}"

# ==========================================================
# ORDER HISTORY
# ==========================================================

class OrderHistory(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="history",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_histories",
    )

    action = models.CharField(
        max_length=200,
        verbose_name="عملیات",
    )

    old_status = models.CharField(
        max_length=30,
        blank=True,
    )

    new_status = models.CharField(
        max_length=30,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "تاریخچه سفارش"

        verbose_name_plural = "تاریخچه سفارش‌ها"

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return f"{self.order.tracking_code} - {self.action}"


# ==========================================================
# ORDER NOTE
# ==========================================================

class OrderNote(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    note = models.TextField()

    private = models.BooleanField(
        default=True,
        verbose_name="خصوصی",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "یادداشت سفارش"

        verbose_name_plural = "یادداشت‌های سفارش"

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return self.order.tracking_code

# ==========================================================
# REVIEW
# ==========================================================

class Review(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="سفارش",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
        verbose_name="کاربر",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name="امتیاز",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="عنوان",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="نظر",
    )

    is_public = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="نمایش عمومی",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "نظر"

        verbose_name_plural = "نظرات"

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return f"{self.order.tracking_code} ({self.rating})"



# ==========================================================
# NOTIFICATION
# ==========================================================

class Notification(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False,
        db_index=True,
    )

    link = models.CharField(
        max_length=300,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "اعلان"

        verbose_name_plural = "اعلان‌ها"

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(fields=["is_read"]),

            models.Index(fields=["created_at"]),

        ]

    def __str__(self):

        return self.title

# ==========================================================
# ENTERPRISE OPTIMIZATION
# ==========================================================

# ----------------------------------------------------------
# SERVICE
# ----------------------------------------------------------

Service._meta.get_field("title").db_index = True
Service._meta.get_field("slug").db_index = True

# ----------------------------------------------------------
# PORTFOLIO
# ----------------------------------------------------------

Portfolio._meta.get_field("slug").db_index = True
Portfolio._meta.get_field("featured").db_index = True
Portfolio._meta.get_field("active").db_index = True

# ----------------------------------------------------------
# ORDER
# ----------------------------------------------------------

Order._meta.indexes += [

    models.Index(

        fields=["tracking_code"],

        name="order_tracking_idx",

    ),

    models.Index(

        fields=["status"],

        name="order_status_idx",

    ),

    models.Index(

        fields=["created_at"],

        name="order_created_idx",

    ),

    models.Index(

        fields=["user"],

        name="order_user_idx",

    ),

]

# ----------------------------------------------------------
# INVOICE
# ----------------------------------------------------------

Invoice._meta.indexes += [

    models.Index(

        fields=["invoice_number"],

        name="invoice_number_idx",

    ),

    models.Index(

        fields=["status"],

        name="invoice_status_idx",

    ),

]

# ----------------------------------------------------------
# TICKET
# ----------------------------------------------------------

Ticket._meta.indexes += [

    models.Index(

        fields=["order"],

        name="ticket_order_idx",

    ),

    models.Index(

        fields=["sender"],

        name="ticket_sender_idx",

    ),

]

# ----------------------------------------------------------
# REVIEW
# ----------------------------------------------------------

Review._meta.indexes += [

    models.Index(

        fields=["rating"],

        name="review_rating_idx",

    ),

]

# ----------------------------------------------------------
# NOTIFICATION
# ----------------------------------------------------------

Notification._meta.indexes += [

    models.Index(

        fields=["user"],

        name="notification_user_idx",

    ),

]

# ----------------------------------------------------------
# DATABASE CONSTRAINTS
# ----------------------------------------------------------

Order._meta.constraints = [

    models.UniqueConstraint(

        fields=["tracking_code"],

        name="unique_tracking_code",

    ),

]

Invoice._meta.constraints = [

    models.UniqueConstraint(

        fields=["invoice_number"],

        name="unique_invoice_number",

    ),

]

Service._meta.constraints = [

    models.UniqueConstraint(

        fields=["slug"],

        name="unique_service_slug",

    ),

]

Portfolio._meta.constraints = [

    models.UniqueConstraint(

        fields=["slug"],

        name="unique_portfolio_slug",

    ),

]

Career._meta.constraints = [

    models.UniqueConstraint(

        fields=["slug"],

        name="unique_career_slug",

    ),

]

# ----------------------------------------------------------
# DEFAULT ORDERING
# ----------------------------------------------------------

Order._meta.ordering = [

    "-created_at",

]

Portfolio._meta.ordering = [

    "-featured",

    "-created_at",

]

Notification._meta.ordering = [

    "-created_at",

]

Ticket._meta.ordering = [

    "created_at",

]

Invoice._meta.ordering = [

    "-created_at",

]

Review._meta.ordering = [

    "-created_at",

]

# ==========================================================
# FINAL ENTERPRISE SETTINGS
# ==========================================================

# این فایل برای موارد زیر آماده است:
#
# ✔ Django Admin
# ✔ Django REST Framework
# ✔ Mobile App
# ✔ React Dashboard
# ✔ PostgreSQL
# ✔ Docker
# ✔ Celery
# ✔ Redis
# ✔ Cloud Storage
# ✔ Payment Gateway
# ✔ SMS
# ✔ Email
# ✔ Notifications
# ✔ Analytics
# ✔ SEO
# ✔ Multi Language
# ✔ Enterprise Scale
#
# ----------------------------------------------------------


# ==========================================================
# ABSTRACT BASE MODEL
# ==========================================================

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        abstract = True


# ==========================================================
# UUID MIXIN
# ==========================================================

class UUIDMixin(models.Model):

    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    class Meta:

        abstract = True


# ==========================================================
# SOFT DELETE (برای آینده)
# ==========================================================

class SoftDeleteModel(models.Model):

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:

        abstract = True


# ==========================================================
# PROJECT VERSION
# ==========================================================

PROJECT_VERSION = "1.0.0 Enterprise"


# ==========================================================
# READY FOR
# ==========================================================

"""
Future Features

✓ API Token

✓ JWT Authentication

✓ OAuth

✓ Google Login

✓ GitHub Login

✓ Two Factor Authentication

✓ SMS Login

✓ Stripe

✓ Zarinpal

✓ IDPay

✓ S3 Storage

✓ Cloudinary

✓ WebSocket

✓ Chat

✓ AI Assistant

✓ CRM

✓ ERP

✓ Team Management

✓ HR

✓ Accounting

✓ Reports

✓ Statistics

✓ Audit Logs

✓ Multi Tenant

✓ White Label
"""

# ==========================================================
# SIGNALS
# ==========================================================

@receiver(post_save, sender=Order)
def create_default_invoice(sender, instance, created, **kwargs):

    if not created:
        return

    Invoice.objects.get_or_create(

        order=instance,

        defaults={

            "amount": instance.estimated_price,

            "due_date": timezone.now().date(),

        },

    )


@receiver(post_save, sender=Order)
def create_order_history(sender, instance, created, **kwargs):

    if created:

        OrderHistory.objects.create(

            order=instance,

            action="Order Created",

            new_status=instance.status,

        )


@receiver(post_save, sender=Ticket)
def notify_new_ticket(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.order.user:

        Notification.objects.create(

            user=instance.order.user,

            title="تیکت جدید",

            message="یک پیام جدید برای سفارش شما ثبت شد.",

            link=reverse(

                "order_detail",

                kwargs={

                    "tracking_code": instance.order.tracking_code,

                },

            ),

        )


@receiver(post_save, sender=ProjectVersion)
def notify_new_version(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.order.user:

        Notification.objects.create(

            user=instance.order.user,

            title="نسخه جدید پروژه",

            message=f"نسخه {instance.version} پروژه شما آماده شد.",

            link=reverse(

                "order_detail",

                kwargs={

                    "tracking_code": instance.order.tracking_code,

                },

            ),

        )


@receiver(post_save, sender=Invoice)
def invoice_paid(sender, instance, **kwargs):

    if instance.status == InvoiceStatus.PAID:

        if instance.paid_at is None:

            instance.paid_at = timezone.now()

            Invoice.objects.filter(

                pk=instance.pk

            ).update(

                paid_at=instance.paid_at

            )


@receiver(post_save, sender=Review)
def review_notification(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.order.user:

        Notification.objects.create(

            user=instance.order.user,

            title="نظر شما ثبت شد",

            message="از ثبت نظر شما سپاسگزاریم.",

        )

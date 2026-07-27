# ==========================================================
# IMPORTS
# ==========================================================

import uuid

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# ==========================================================
# BASE MODEL
# ==========================================================

class BaseModel(models.Model):
    """
    Base model for all accounts models.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


# ==========================================================
# VALIDATORS
# ==========================================================

phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{10,15}$",
    message=_("شماره موبایل معتبر نیست."),
)


# ==========================================================
# USER ROLE
# ==========================================================

class UserRole(models.TextChoices):

    CLIENT = "client", _("مشتری")

    DESIGNER = "designer", _("طراح")

    DEVELOPER = "developer", _("برنامه نویس")

    MANAGER = "manager", _("مدیر")


# ==========================================================
# GENDER
# ==========================================================

class Gender(models.TextChoices):

    MALE = "male", _("مرد")

    FEMALE = "female", _("زن")

    OTHER = "other", _("سایر")


# ==========================================================
# NOTIFICATION TYPE
# ==========================================================

class NotificationType(models.TextChoices):

    SYSTEM = "system", _("سیستم")

    ORDER = "order", _("سفارش")

    PAYMENT = "payment", _("پرداخت")

    SUPPORT = "support", _("پشتیبانی")

    ACCOUNT = "account", _("حساب کاربری")


# ==========================================================
# NOTIFICATION PRIORITY
# ==========================================================

class NotificationPriority(models.TextChoices):

    LOW = "low", _("کم")

    NORMAL = "normal", _("عادی")

    HIGH = "high", _("زیاد")

    URGENT = "urgent", _("فوری")


# ==========================================================
# ADDRESS TYPE
# ==========================================================

class AddressType(models.TextChoices):

    HOME = "home", _("خانه")

    WORK = "work", _("محل کار")

    BILLING = "billing", _("صورتحساب")

    SHIPPING = "shipping", _("ارسال")


# ==========================================================
# ACTIVITY TYPE
# ==========================================================

class ActivityType(models.TextChoices):

    LOGIN = "login", _("ورود")

    LOGOUT = "logout", _("خروج")

    REGISTER = "register", _("ثبت نام")

    PROFILE = "profile", _("ویرایش پروفایل")

    PASSWORD = "password", _("تغییر رمز عبور")

    ORDER = "order", _("سفارش")

    PAYMENT = "payment", _("پرداخت")

    SUPPORT = "support", _("پشتیبانی")

# ==========================================================
# USER PROFILE
# ==========================================================

class UserProfile(BaseModel):

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="profile",

    )

    avatar = models.ImageField(

        upload_to="avatars/%Y/%m/",

        blank=True,

        null=True,

    )

    phone = models.CharField(

        max_length=15,

        validators=[phone_validator],

        unique=True,

        blank=True,

        null=True,

        db_index=True,

    )

    bio = models.TextField(

        max_length=1000,

        blank=True,

    )

    birthday = models.DateField(

        blank=True,

        null=True,

    )

    gender = models.CharField(

        max_length=10,

        choices=Gender.choices,

        blank=True,

    )

    role = models.CharField(

        max_length=20,

        choices=UserRole.choices,

        default=UserRole.CLIENT,

        db_index=True,

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

    telegram = models.URLField(

        blank=True,

    )

    instagram = models.URLField(

        blank=True,

    )

    email_verified = models.BooleanField(

        default=False,

        db_index=True,

    )

    is_profile_completed = models.BooleanField(

        default=False,

    )

    receive_notifications = models.BooleanField(

        default=True,

    )

    receive_marketing_emails = models.BooleanField(

        default=False,

    )

    preferred_language = models.CharField(

        max_length=20,

        default="fa",

    )

    timezone = models.CharField(

        max_length=50,

        default="Asia/Tehran",

    )

    last_seen = models.DateTimeField(

        blank=True,

        null=True,

    )

    class Meta:

        verbose_name = "پروفایل کاربر"

        verbose_name_plural = "پروفایل کاربران"

        ordering = ["user__username"]

        indexes = [

            models.Index(fields=["role"]),

            models.Index(fields=["phone"]),

            models.Index(fields=["email_verified"]),

        ]

    def __str__(self):

        return f"{self.user.username}"

    @property
    def full_name(self):

        return (

            self.user.get_full_name()

            or self.user.username

        )

    @property
    def display_name(self):

        if self.user.first_name:

            return self.user.get_full_name()

        return self.user.username

# ==========================================================
# EMAIL VERIFICATION TOKEN
# ==========================================================

class EmailVerificationToken(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="email_tokens",

    )

    token = models.UUIDField(

        default=uuid.uuid4,

        unique=True,

        editable=False,

    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(

        default=False,

    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "توکن تایید ایمیل"

        verbose_name_plural = "توکن‌های تایید ایمیل"

    def __str__(self):

        return f"{self.user.username} - Email Verify"

    @property
    def is_expired(self):

        return timezone.now() >= self.expires_at


# ==========================================================
# PASSWORD RESET TOKEN
# ==========================================================

class PasswordResetToken(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="password_tokens",

    )

    token = models.UUIDField(

        default=uuid.uuid4,

        unique=True,

        editable=False,

    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(

        default=False,

    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "توکن بازیابی رمز"

        verbose_name_plural = "توکن‌های بازیابی رمز"

    @property
    def is_expired(self):

        return timezone.now() >= self.expires_at


# ==========================================================
# LOGIN HISTORY
# ==========================================================

class LoginHistory(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="login_history",

    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    browser = models.CharField(

        max_length=100,

        blank=True,

    )

    operating_system = models.CharField(

        max_length=100,

        blank=True,

    )

    device = models.CharField(

        max_length=100,

        blank=True,

    )

    success = models.BooleanField(

        default=True,

        db_index=True,

    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "تاریخچه ورود"

        verbose_name_plural = "تاریخچه ورود"

        indexes = [

            models.Index(fields=["user", "success"]),

        ]

    def __str__(self):

        return f"{self.user.username} - {self.created_at}"


# ==========================================================
# FAILED LOGIN
# ==========================================================

class FailedLoginAttempt(BaseModel):

    username = models.CharField(

        max_length=150,

        db_index=True,

    )

    ip_address = models.GenericIPAddressField(

        db_index=True,

    )

    user_agent = models.TextField()

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "ورود ناموفق"

        verbose_name_plural = "ورودهای ناموفق"

# ==========================================================
# ADDRESS
# ==========================================================

class Address(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="addresses",

    )

    title = models.CharField(

        max_length=100,

        help_text="مثال: خانه، محل کار",

    )

    address_type = models.CharField(

        max_length=20,

        choices=AddressType.choices,

        default=AddressType.HOME,

        db_index=True,

    )

    full_name = models.CharField(

        max_length=150,

    )

    phone = models.CharField(

        max_length=15,

        validators=[phone_validator],

    )

    country = models.CharField(

        max_length=100,

        default="Iran",

    )

    province = models.CharField(

        max_length=100,

    )

    city = models.CharField(

        max_length=100,

    )

    postal_code = models.CharField(

        max_length=20,

        blank=True,

    )

    address = models.TextField()

    latitude = models.DecimalField(

        max_digits=9,

        decimal_places=6,

        blank=True,

        null=True,

    )

    longitude = models.DecimalField(

        max_digits=9,

        decimal_places=6,

        blank=True,

        null=True,

    )

    is_default = models.BooleanField(

        default=False,

        db_index=True,

    )

    is_active = models.BooleanField(

        default=True,

        db_index=True,

    )

    notes = models.TextField(

        blank=True,

    )

    class Meta:

        verbose_name = "آدرس"

        verbose_name_plural = "آدرس‌ها"

        ordering = [

            "-is_default",

            "-created_at",

        ]

        indexes = [

            models.Index(

                fields=[

                    "user",

                    "is_default",

                ]

            ),

            models.Index(

                fields=[

                    "province",

                    "city",

                ]

            ),

            models.Index(

                fields=[

                    "is_active",

                ]

            ),

        ]

        constraints = [

            models.UniqueConstraint(

                fields=[

                    "user",

                    "title",

                ],

                name="unique_user_address_title",

            ),

        ]

    def __str__(self):

        return (

            f"{self.user.username} - "

            f"{self.title}"

        )

    @property
    def short_address(self):

        return (

            f"{self.city} - "

            f"{self.province}"

        )

    @property
    def full_address(self):

        return (

            f"{self.country}, "

            f"{self.province}, "

            f"{self.city}, "

            f"{self.address}"

        )

# ==========================================================
# NOTIFICATION
# ==========================================================

class Notification(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="account_notifications",

    )

    title = models.CharField(

        max_length=200,

    )

    message = models.TextField()

    notification_type = models.CharField(

        max_length=20,

        choices=NotificationType.choices,

        default=NotificationType.SYSTEM,

        db_index=True,

    )

    priority = models.CharField(

        max_length=20,

        choices=NotificationPriority.choices,

        default=NotificationPriority.NORMAL,

        db_index=True,

    )

    icon = models.CharField(

        max_length=100,

        blank=True,

        help_text="FontAwesome icon",

    )

    color = models.CharField(

        max_length=30,

        default="primary",

        help_text="Bootstrap color",

    )

    action_url = models.CharField(

        max_length=255,

        blank=True,

        help_text="Redirect URL",

    )

    is_read = models.BooleanField(

        default=False,

        db_index=True,

    )

    read_at = models.DateTimeField(

        blank=True,

        null=True,

    )

    expires_at = models.DateTimeField(

        blank=True,

        null=True,

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

                ]

            ),

            models.Index(

                fields=[

                    "priority",

                ]

            ),

            models.Index(

                fields=[

                    "expires_at",

                ]

            ),

        ]

    def __str__(self):

        return (

            f"{self.user.username} - "

            f"{self.title}"

        )

    @property
    def expired(self):

        if not self.expires_at:

            return False

        return timezone.now() >= self.expires_at

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

    def mark_as_unread(self):

        self.is_read = False

        self.read_at = None

        self.save(

            update_fields=[

                "is_read",

                "read_at",

            ]

        )

class NotificationSettings(BaseModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_settings",
        verbose_name="کاربر",
    )

    email_notifications = models.BooleanField(
        default=True,
        verbose_name="اعلان ایمیلی",
    )

    order_notifications = models.BooleanField(
        default=True,
        verbose_name="اعلان سفارش‌ها",
    )

    payment_notifications = models.BooleanField(
        default=True,
        verbose_name="اعلان پرداخت‌ها",
    )

    system_notifications = models.BooleanField(
        default=True,
        verbose_name="اعلان‌های سیستمی",
    )

    marketing_emails = models.BooleanField(
        default=True,
        verbose_name="ایمیل‌های تبلیغاتی"
    )

    security_alerts = models.BooleanField(
        default=True,
        verbose_name="هشدارهای امنیتی"
    )

    order_updates = models.BooleanField(
        default=True,
        verbose_name="به‌روزرسانی سفارش‌ها"
    )

    class Meta:

        verbose_name = "تنظیمات اعلان"

        verbose_name_plural = "تنظیمات اعلان‌ها"


    def __str__(self):

        return f"تنظیمات اعلان {self.user.username}"

# ==========================================================
# ACTIVITY LOG
# ==========================================================

class ActivityLog(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="activities",

    )

    action = models.CharField(

        max_length=50,

        choices=ActivityType.choices,

        db_index=True,

    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(

        blank=True,

        null=True,

        db_index=True,

    )

    user_agent = models.TextField(

        blank=True,

    )

    browser = models.CharField(

        max_length=100,

        blank=True,

    )

    operating_system = models.CharField(

        max_length=100,

        blank=True,

    )

    device = models.CharField(

        max_length=100,

        blank=True,

    )

    path = models.CharField(

        max_length=255,

        blank=True,

    )

    method = models.CharField(

        max_length=10,

        blank=True,

    )

    metadata = models.JSONField(

        default=dict,

        blank=True,

    )

    class Meta:

        verbose_name = "گزارش فعالیت"

        verbose_name_plural = "گزارش فعالیت‌ها"

        ordering = [

            "-created_at",

        ]

        indexes = [

            models.Index(

                fields=[

                    "user",

                    "action",

                ]

            ),

            models.Index(

                fields=[

                    "created_at",

                ]

            ),

            models.Index(

                fields=[

                    "ip_address",

                ]

            ),

        ]

    def __str__(self):

        return (

            f"{self.user.username} | "

            f"{self.action} | "

            f"{self.created_at:%Y-%m-%d %H:%M}"

        )

    @property
    def short_description(self):

        if len(self.description) <= 80:

            return self.description

        return self.description[:80] + "..."

    @property
    def is_login_activity(self):

        return self.action == ActivityType.LOGIN

    @property
    def is_security_activity(self):

        return self.action in [

            ActivityType.LOGIN,

            ActivityType.LOGOUT,

            ActivityType.PASSWORD,

            ActivityType.REGISTER,

        ]

# ==========================================================
# DEPARTMENT
# ==========================================================

class Department(BaseModel):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    color = models.CharField(
        max_length=20,
        default="primary",
        help_text="Bootstrap color",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="FontAwesome icon",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    department_type = models.CharField(
        max_length=100,
        verbose_name="نوع دپارتمان"
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_departments",
        verbose_name="مدیر دپارتمان"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش"
    )

    class Meta:

        verbose_name = "دپارتمان"

        verbose_name_plural = "دپارتمان‌ها"

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name


# ==========================================================
# EMPLOYEE
# ==========================================================

class Employee(BaseModel):

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="employee",

    )

    department = models.ForeignKey(

        Department,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="employees",

    )

    manager = models.ForeignKey(

        "self",

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="team_members",

    )

    employee_code = models.CharField(

        max_length=30,

        unique=True,

    )

    job_title = models.CharField(

        max_length=150,

    )

    hired_at = models.DateField()

    salary = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0,

    )

    active = models.BooleanField(

        default=True,

        db_index=True,

    )

    emergency_phone = models.CharField(

        max_length=15,

        validators=[phone_validator],

        blank=True,

    )

    notes = models.TextField(

        blank=True,

    )
    
    position = models.CharField(
        max_length=100,
        verbose_name="سمت"
    )

    skills = models.TextField(
        blank=True,
        verbose_name="مهارت‌ها"
    )

    github = models.URLField(
        blank=True,
        verbose_name="گیت‌هاب"
    )

    linkedin = models.URLField(
        blank=True,
        verbose_name="لینکدین"
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name="آماده همکاری"
    )

    class Meta:

        verbose_name = "کارمند"

        verbose_name_plural = "کارمندان"

        ordering = [
            "user__username",
        ]

        indexes = [

            models.Index(
                fields=[
                    "department",
                ]
            ),

            models.Index(
                fields=[
                    "active",
                ]
            ),

        ]

    def __str__(self):

        return (

            self.user.get_full_name()

            or self.user.username

        )

    @property
    def full_name(self):

        return (

            self.user.get_full_name()

            or self.user.username

        )

    @property
    def is_manager(self):

        return self.user.profile.role == UserRole.MANAGER

    @property
    def team_size(self):

        return self.team_members.count()

# ==========================================================
# TICKET STATUS
# ==========================================================

class TicketStatus(models.TextChoices):

    OPEN = "open", _("باز")

    IN_PROGRESS = "in_progress", _("در حال بررسی")

    WAITING = "waiting", _("در انتظار پاسخ کاربر")

    RESOLVED = "resolved", _("حل شده")

    CLOSED = "closed", _("بسته شده")


# ==========================================================
# TICKET PRIORITY
# ==========================================================

class TicketPriority(models.TextChoices):

    LOW = "low", _("کم")

    NORMAL = "normal", _("عادی")

    HIGH = "high", _("زیاد")

    URGENT = "urgent", _("فوری")


# ==========================================================
# TICKET
# ==========================================================

class Ticket(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="account_tickets",

    )

    assigned_to = models.ForeignKey(

        Employee,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="assigned_tickets",

    )

    title = models.CharField(

        max_length=200,

    )

    message = models.TextField()

    priority = models.CharField(

        max_length=20,

        choices=TicketPriority.choices,

        default=TicketPriority.NORMAL,

        db_index=True,

    )

    status = models.CharField(

        max_length=30,

        choices=TicketStatus.choices,

        default=TicketStatus.OPEN,

        db_index=True,

    )

    closed_at = models.DateTimeField(

        blank=True,

        null=True,

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

                ]

            ),

        ]

    def __str__(self):

        return f"#{self.pk} - {self.title}"


# ==========================================================
# TICKET REPLY
# ==========================================================

class TicketReply(BaseModel):

    ticket = models.ForeignKey(

        Ticket,

        on_delete=models.CASCADE,

        related_name="replies",

    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

    )

    message = models.TextField()

    is_staff_reply = models.BooleanField(

        default=False,

    )

    class Meta:

        verbose_name = "پاسخ تیکت"

        verbose_name_plural = "پاسخ‌های تیکت"

        ordering = [

            "created_at",

        ]

    def __str__(self):

        return f"Reply #{self.pk}"


# ==========================================================
# TICKET ATTACHMENT
# ==========================================================

class TicketAttachment(BaseModel):

    ticket = models.ForeignKey(

        Ticket,

        on_delete=models.CASCADE,

        related_name="attachments",

    )

    file = models.FileField(

        upload_to="tickets/%Y/%m/",

    )

    uploaded_by = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

    )

    class Meta:

        verbose_name = "فایل تیکت"

        verbose_name_plural = "فایل‌های تیکت"

    def __str__(self):

        return self.file.name

# ==========================================================
# PAYMENT STATUS
# ==========================================================

class PaymentStatus(models.TextChoices):

    PENDING = "pending", _("در انتظار پرداخت")

    PAID = "paid", _("پرداخت شده")

    FAILED = "failed", _("ناموفق")

    REFUNDED = "refunded", _("بازگشت وجه")

    CANCELLED = "cancelled", _("لغو شده")


# ==========================================================
# PAYMENT METHOD
# ==========================================================

class PaymentMethod(models.TextChoices):

    CARD = "card", _("کارت بانکی")

    WALLET = "wallet", _("کیف پول")

    BANK = "bank", _("انتقال بانکی")

    CASH = "cash", _("نقدی")


# ==========================================================
# INVOICE
# ==========================================================

class Invoice(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="invoices",

    )

    invoice_number = models.CharField(

        max_length=50,

        unique=True,

        db_index=True,

    )

    subtotal = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    discount = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0,

    )

    tax = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0,

    )

    total = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    status = models.CharField(

        max_length=20,

        choices=PaymentStatus.choices,

        default=PaymentStatus.PENDING,

        db_index=True,

    )

    issued_at = models.DateTimeField(

        auto_now_add=True,

    )

    due_date = models.DateField(

        blank=True,

        null=True,

    )

    class Meta:

        verbose_name = "فاکتور"

        verbose_name_plural = "فاکتورها"

        ordering = [

            "-issued_at",

        ]

        indexes = [

            models.Index(fields=["invoice_number"]),

            models.Index(fields=["status"]),

        ]

    def __str__(self):

        return self.invoice_number


# ==========================================================
# PAYMENT
# ==========================================================

class Payment(BaseModel):

    invoice = models.OneToOneField(

        Invoice,

        on_delete=models.CASCADE,

        related_name="payment",

    )

    method = models.CharField(

        max_length=20,

        choices=PaymentMethod.choices,

        default=PaymentMethod.CARD,

    )

    status = models.CharField(

        max_length=20,

        choices=PaymentStatus.choices,

        default=PaymentStatus.PENDING,

        db_index=True,

    )

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    paid_at = models.DateTimeField(

        blank=True,

        null=True,

    )

    class Meta:

        verbose_name = "پرداخت"

        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):

        return f"{self.invoice.invoice_number}"


# ==========================================================
# TRANSACTION
# ==========================================================

class Transaction(BaseModel):

    payment = models.ForeignKey(

        Payment,

        on_delete=models.CASCADE,

        related_name="transactions",

    )

    authority = models.CharField(

        max_length=100,

        unique=True,

        db_index=True,

    )

    reference_id = models.CharField(

        max_length=100,

        blank=True,

    )

    gateway = models.CharField(

        max_length=100,

        default="ZarinPal",

    )

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2,

    )

    success = models.BooleanField(

        default=False,

        db_index=True,

    )

    raw_response = models.JSONField(

        default=dict,

        blank=True,

    )

    class Meta:

        verbose_name = "تراکنش"

        verbose_name_plural = "تراکنش‌ها"

        ordering = [

            "-created_at",

        ]

        indexes = [

            models.Index(fields=["authority"]),

            models.Index(fields=["success"]),

        ]

    def __str__(self):

        return self.authority

# ==========================================================
# PROJECT STATUS
# ==========================================================

class ProjectStatus(models.TextChoices):

    PLANNING = "planning", _("برنامه‌ریزی")

    DEVELOPMENT = "development", _("در حال توسعه")

    TESTING = "testing", _("در حال تست")

    DEPLOYMENT = "deployment", _("آماده انتشار")

    COMPLETED = "completed", _("تکمیل شده")


# ==========================================================
# PROJECT TIMELINE
# ==========================================================

class Timeline(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="account_timeline",

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


# ==========================================================
# PROJECT PROGRESS
# ==========================================================

class ProjectProgress(BaseModel):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="project_progress",

    )

    project_name = models.CharField(

        max_length=200,

    )

    progress = models.PositiveSmallIntegerField(

        default=0,

    )

    current_step = models.CharField(

        max_length=200,

    )

    status = models.CharField(

        max_length=30,

        choices=ProjectStatus.choices,

        default=ProjectStatus.PLANNING,

    )

    class Meta:

        verbose_name = "پیشرفت پروژه"

        verbose_name_plural = "پیشرفت پروژه‌ها"

        ordering = [

            "-updated_at",
        ]

        constraints = [

            models.CheckConstraint(

                condition=models.Q(progress__gte=0) & models.Q(progress__lte=100),

                name="progress_between_0_100",
            )
        ]
    def __str__(self):

        return f"{self.project_name} ({self.progress}%)"
# ==========================================================
# VERSION HISTORY
# ==========================================================

class VersionHistory(BaseModel):

    version = models.CharField(

        max_length=30,

        unique=True,
    )

    title = models.CharField(

        max_length=200,
    )

    description = models.TextField()

    released_at = models.DateTimeField(

        default=timezone.now,
    )

    is_stable = models.BooleanField(

        default=True,

        db_index=True,
    )

    class Meta:

        verbose_name = "نسخه"

        verbose_name_plural = "نسخه‌ها"

        ordering = [

            "-released_at",
        ]

    def __str__(self):

        return self.version

# ==========================================================
# CUSTOM QUERYSETS
# ==========================================================

class UserProfileQuerySet(models.QuerySet):

    def verified(self):
        return self.filter(email_verified=True)

    def unverified(self):
        return self.filter(email_verified=False)

    def managers(self):
        return self.filter(role=UserRole.MANAGER)

    def developers(self):
        return self.filter(role=UserRole.DEVELOPER)

    def designers(self):
        return self.filter(role=UserRole.DESIGNER)

    def clients(self):
        return self.filter(role=UserRole.CLIENT)


class NotificationQuerySet(models.QuerySet):

    def unread(self):
        return self.filter(is_read=False)

    def read(self):
        return self.filter(is_read=True)

    def active(self):
        return self.filter(
            models.Q(expires_at__isnull=True)
            | models.Q(expires_at__gt=timezone.now())
        )


class TicketQuerySet(models.QuerySet):

    def open(self):
        return self.filter(status=TicketStatus.OPEN)

    def closed(self):
        return self.filter(status=TicketStatus.CLOSED)

    def active(self):
        return self.exclude(status=TicketStatus.CLOSED)


class ActivityLogQuerySet(models.QuerySet):

    def today(self):
        return self.filter(created_at__date=timezone.now().date())

    def by_user(self, user):
        return self.filter(user=user)

    def security(self):
        return self.filter(
            action__in=[
                ActivityType.LOGIN,
                ActivityType.LOGOUT,
                ActivityType.PASSWORD,
                ActivityType.REGISTER,
            ]
        )


# ==========================================================
# CUSTOM MANAGERS
# ==========================================================

class UserProfileManager(models.Manager):

    def get_queryset(self):
        return UserProfileQuerySet(
            self.model,
            using=self._db,
        )

    def verified(self):
        return self.get_queryset().verified()

    def managers(self):
        return self.get_queryset().managers()


class NotificationManager(models.Manager):

    def get_queryset(self):
        return NotificationQuerySet(
            self.model,
            using=self._db,
        )

    def unread(self):
        return self.get_queryset().unread()


class TicketManager(models.Manager):

    def get_queryset(self):
        return TicketQuerySet(
            self.model,
            using=self._db,
        )

    def open(self):
        return self.get_queryset().open()


class ActivityLogManager(models.Manager):

    def get_queryset(self):
        return ActivityLogQuerySet(
            self.model,
            using=self._db,
        )

    def today(self):
        return self.get_queryset().today()


# ==========================================================
# ATTACH MANAGERS
# ==========================================================

UserProfile.add_to_class(
    "objects",
    UserProfileManager(),
)

Notification.add_to_class(
    "objects",
    NotificationManager(),
)

Ticket.add_to_class(
    "objects",
    TicketManager(),
)

ActivityLog.add_to_class(
    "objects",
    ActivityLogManager(),
)

# ==========================================================
# MODEL HELPERS
# ==========================================================

def generate_invoice_number():

    today = timezone.now().strftime("%Y%m%d")

    random_part = uuid.uuid4().hex[:8].upper()

    return f"INV-{today}-{random_part}"


def generate_employee_code():

    random_part = uuid.uuid4().hex[:6].upper()

    return f"EMP-{random_part}"


# ==========================================================
# MODEL UTILITIES
# ==========================================================

class ModelUtils:

    @staticmethod
    def mark_notification_read(notification):

        if not notification.is_read:

            notification.is_read = True

            notification.read_at = timezone.now()

            notification.save(
                update_fields=[
                    "is_read",
                    "read_at",
                ]
            )

    @staticmethod
    def close_ticket(ticket):

        ticket.status = TicketStatus.CLOSED

        ticket.closed_at = timezone.now()

        ticket.save(
            update_fields=[
                "status",
                "closed_at",
            ]
        )

class UserActivityLog(models.Model):

    ACTION_CHOICES = (

        ("register", "ثبت‌نام"),

        ("login", "ورود"),

        ("logout", "خروج"),

        ("profile_update", "ویرایش پروفایل"),

        ("password_change", "تغییر رمز عبور"),

        ("order_create", "ایجاد سفارش"),

        ("order_cancel", "لغو سفارش"),

        ("ticket_create", "ایجاد تیکت"),

        ("ticket_reply", "پاسخ به تیکت"),

        ("invoice_download", "دانلود فاکتور"),

        ("security", "امنیت"),

        ("other", "سایر"),

    )


    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="activity_logs",

        verbose_name="کاربر",

    )


    action = models.CharField(

        max_length=50,

        choices=ACTION_CHOICES,

        db_index=True,

        verbose_name="نوع فعالیت",

    )


    description = models.TextField(

        blank=True,

        verbose_name="توضیحات",

    )


    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True,

        verbose_name="آدرس IP",

    )


    user_agent = models.TextField(

        blank=True,

        verbose_name="User Agent",

    )


    created_at = models.DateTimeField(

        auto_now_add=True,

        db_index=True,

        verbose_name="زمان ثبت",

    )


    class Meta:

        verbose_name = "لاگ فعالیت کاربر"

        verbose_name_plural = "لاگ‌های فعالیت کاربران"

        ordering = [

            "-created_at",

        ]


    def __str__(self):

        return (

            f"{self.user} - "

            f"{self.get_action_display()}"

        )

# ==========================================================
# DEFAULT ORDERING CHECK
# ==========================================================

ALL_ACCOUNT_MODELS = [

    UserProfile,

    EmailVerificationToken,

    PasswordResetToken,

    LoginHistory,

    FailedLoginAttempt,

    Address,

    Notification,

    ActivityLog,

    Department,

    Employee,

    Ticket,

    TicketReply,

    TicketAttachment,

    Invoice,

    Payment,

    Transaction,

    Timeline,

    ProjectProgress,

    VersionHistory,
]

# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "BaseModel",

    "UserProfile",

    "EmailVerificationToken",

    "PasswordResetToken",

    "LoginHistory",

    "FailedLoginAttempt",

    "Address",

    "Notification",

    "ActivityLog",

    "Department",

    "Employee",

    "Ticket",

    "TicketReply",

    "TicketAttachment",

    "Invoice",

    "Payment",

    "Transaction",

    "Timeline",

    "ProjectProgress",

    "VersionHistory",

    "UserRole",

    "Gender",

    "NotificationType",

    "NotificationPriority",

    "AddressType",

    "ActivityType",

    "TicketStatus",

    "TicketPriority",

    "PaymentStatus",

    "PaymentMethod",

    "ProjectStatus",

    "generate_invoice_number",

    "generate_employee_code",

    "ModelUtils",

]
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.utils import timezone

from .models import (
    Service,
    Portfolio,
    Order,
    Contact,
    Career,
    JobApplication,
    Ticket,
    Invoice,
    ProjectProgress,
    ProjectTimeline,
    ProjectTask,
    ProjectVersion,
)

# ==========================================================
# ADMIN HELPERS
# ==========================================================

def image_preview(obj):

    if getattr(obj, "image", None):

        return format_html(

            '<img src="{}" width="90" '
            'style="border-radius:10px;'
            'border:1px solid #ddd;">',

            obj.image.url,

        )

    return "-"


image_preview.short_description = "پیش نمایش"


def order_status_badge(obj):

    colors = {

        "pending": "#ffc107",

        "processing": "#0dcaf0",

        "completed": "#198754",

        "cancelled": "#dc3545",

    }

    labels = {

        "pending": "در انتظار",

        "processing": "در حال انجام",

        "completed": "تکمیل شده",

        "cancelled": "لغو شده",

    }

    return format_html(

        '<span style="'
        'background:{};'
        'color:white;'
        'padding:5px 12px;'
        'border-radius:15px;'
        'font-size:12px;'
        'font-weight:bold;">'
        '{}'
        '</span>',

        colors.get(obj.status, "#6c757d"),

        labels.get(obj.status, obj.status),

    )


order_status_badge.short_description = "وضعیت"


def progress_badge(obj):

    value = getattr(obj, "percent", 0)

    color = "#dc3545"

    if value >= 30:
        color = "#ffc107"

    if value >= 70:
        color = "#0dcaf0"

    if value == 100:
        color = "#198754"

    return format_html(

        '<strong style="color:{};">{}%</strong>',

        color,

        value,

    )


progress_badge.short_description = "پیشرفت"


def file_download(obj):

    if hasattr(obj, "file") and obj.file:

        return format_html(

            '<a class="button" href="{}" target="_blank">'
            'دانلود'
            '</a>',

            obj.file.url,

        )

    return "-"


file_download.short_description = "فایل"

# ==========================================================
# SERVICE ADMIN
# ==========================================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (

        "title",

        "base_price",

        "active",

        "portfolio_count",

        "created_at",

    )

    list_display_links = (

        "title",

    )

    list_editable = (

        "active",

    )

    search_fields = (

        "title",

        "description",

    )

    list_filter = (

        "active",

        "created_at",

    )

    ordering = (

        "title",

    )

    readonly_fields = (

        "created_at",

        "updated_at",

    )

    list_per_page = 20

    save_on_top = True

    prepopulated_fields = {

        "slug": ("title",)

    }

    fieldsets = (

        (

            "اطلاعات اصلی",

            {

                "fields": (

                    "title",

                    "slug",

                    "description",

                )

            },

        ),

        (

            "تنظیمات",

            {

                "fields": (

                    "base_price",

                    "icon",

                    "active",

                )

            },

        ),

        (

            "اطلاعات سیستم",

            {

                "classes": (

                    "collapse",

                ),

                "fields": (

                    "created_at",

                    "updated_at",

                ),

            },

        ),

    )

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return queryset.annotate(

            total_portfolios=Count("portfolios")

        )

    @admin.display(

        description="نمونه کارها",

        ordering="total_portfolios",

    )

    def portfolio_count(self, obj):

        return obj.total_portfolios

# ==========================================================
# PORTFOLIO ADMIN
# ==========================================================

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):

    list_display = (

        "image_preview",

        "title",

        "service",

        "client",

        "featured",

        "views",

        "created_at",

    )

    list_display_links = (

        "image_preview",

        "title",

    )

    list_editable = (

        "featured",

    )

    search_fields = (

        "title",

        "description",

        "client",

        "technologies",

    )

    list_filter = (

        "featured",

        "service",

        "created_at",

    )

    autocomplete_fields = (

        "service",

    )

    readonly_fields = (

        "image_preview",

        "views",

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 20

    save_on_top = True

    prepopulated_fields = {

        "slug": ("title",)

    }

    fieldsets = (

        (

            "اطلاعات پروژه",

            {

                "fields": (

                    "title",

                    "slug",

                    "description",

                    "service",

                )

            },

        ),

        (

            "رسانه",

            {

                "fields": (

                    "image",

                    "image_preview",

                )

            },

        ),

        (

            "اطلاعات تکمیلی",

            {

                "fields": (

                    "client",

                    "technologies",

                    "featured",

                )

            },

        ),

        (

            "آمار",

            {

                "classes": (

                    "collapse",

                ),

                "fields": (

                    "views",

                    "created_at",

                ),

            },

        ),

    )

    @admin.display(description="تصویر")

    def image_preview(self, obj):

        return image_preview(obj)

# ==========================================================
# ADMIN INLINES
# ==========================================================

class TicketInline(admin.TabularInline):

    model = Ticket

    extra = 0

    fields = (

        "sender",

        "message",

        "attachment",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    show_change_link = True



class ProjectProgressInline(admin.TabularInline):
    model = ProjectProgress

    extra = 0

    fields = (

        "title",

        "percent",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    show_change_link = True



class ProjectTimelineInline(admin.TabularInline):
    model = ProjectTimeline

    extra = 0

    fields = (

        "title",

        "completed",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    show_change_link = True



class ProjectTaskInline(admin.TabularInline):
    model = ProjectTask

    extra = 0

    fields = (

        "title",

        "status",

        "deadline",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    show_change_link = True



class ProjectVersionInline(admin.TabularInline):
    model = ProjectVersion

    extra = 0

    fields = (

        "version",

        "file",

        "description",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    show_change_link = True

# ==========================================================
# ORDER ADMIN
# ==========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        "tracking_code",

        "full_name",

        "service",

        "order_status_badge",

        "estimated_price",

        "created_at",

    )

    list_display_links = (

        "tracking_code",

        "full_name",

    )

    list_filter = (

        "status",

        "service",

        "created_at",

    )

    search_fields = (

        "tracking_code",

        "full_name",

        "phone",

        "email",

        "description",

    )

    autocomplete_fields = (

        "user",

        "service",

    )

    readonly_fields = (

        "tracking_code",

        "estimated_price",

        "created_at",

        "updated_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 25

    save_on_top = True

    actions = (

        "mark_processing",

        "mark_completed",

        "mark_cancelled",

    )

    inlines = (

        TicketInline,
        ProjectProgressInline,
        ProjectTimelineInline,
        ProjectTaskInline,
        ProjectVersionInline,

    )

    fieldsets = (

        (

            "اطلاعات مشتری",

            {

                "fields": (

                    "user",

                    "full_name",

                    "phone",

                    "email",

                )

            },

        ),

        (

            "اطلاعات سفارش",

            {

                "fields": (

                    "service",

                    "description",

                    "attachment",

                )

            },

        ),

        (

            "مدیریت پروژه",

            {

                "fields": (

                    "status",

                    "estimated_price",

                    "tracking_code",

                )

            },

        ),

        (

            "اطلاعات سیستم",

            {

                "classes": (

                    "collapse",

                ),

                "fields": (

                    "created_at",

                    "updated_at",

                ),

            },

        ),

    )

    @admin.display(

        description="وضعیت"

    )

    def order_status_badge(self, obj):

        return order_status_badge(obj)

    @admin.action(

        description="تغییر وضعیت به در حال انجام"

    )

    def mark_processing(

        self,

        request,

        queryset,

    ):

        queryset.update(

            status="processing"

        )

    @admin.action(

        description="تغییر وضعیت به تکمیل شده"

    )

    def mark_completed(

        self,

        request,

        queryset,

    ):

        queryset.update(

            status="completed"

        )

    @admin.action(

        description="تغییر وضعیت به لغو شده"

    )

    def mark_cancelled(

        self,

        request,

        queryset,

    ):

        queryset.update(

            status="cancelled"
        )

    def get_queryset(

        self,

        request,

    ):

        return (

            super()

            .get_queryset(request)

            .select_related(

                "user",

                "service",

            )

        )

# ==========================================================
# TICKET ADMIN
# ==========================================================

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "sender",

        "created_at",

    )

    list_display_links = (

        "order",

    )

    search_fields = (

        "order__tracking_code",

        "sender__username",

        "message",

    )

    list_filter = (

        "created_at",

    )

    autocomplete_fields = (

        "order",

        "sender",

    )

    readonly_fields = (

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True


# ==========================================================
# PROGRESS ADMIN
# ==========================================================

@admin.register(ProjectProgress)
class ProgressAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "title",

        "progress_badge",

        "created_at",

    )

    list_display_links = (

        "title",

    )

    search_fields = (

        "title",

        "description",

        "order__tracking_code",

    )

    list_filter = (

        "created_at",

    )

    autocomplete_fields = (

        "order",

    )

    readonly_fields = (

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True

    @admin.display(description="پیشرفت")

    def progress_badge(self, obj):

        return progress_badge(obj)


# ==========================================================
# TIMELINE ADMIN
# ==========================================================

@admin.register(ProjectTimeline)
class TimelineAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "title",
        "created_at",
    )

    list_display_links = (

        "title",

    )

    search_fields = (

        "title",

        "description",

        "order__tracking_code",

    )

    list_filter = (
        "created_at",
    )

    autocomplete_fields = (

        "order",

    )

    readonly_fields = (

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True

# ==========================================================
# TASK ADMIN
# ==========================================================

@admin.register(ProjectTask)
class TaskAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "title",

        "status",

        "deadline",

        "created_at",

    )

    list_display_links = (

        "title",

    )

    list_editable = (

        "status",

    )

    search_fields = (

        "title",

        "description",

        "order__tracking_code",

    )

    list_filter = (

        "status",

        "deadline",

        "created_at",

    )

    autocomplete_fields = (

        "order",

    )

    readonly_fields = (

        "created_at",

        "updated_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True


# ==========================================================
# VERSION ADMIN
# ==========================================================

@admin.register(ProjectVersion)
class VersionAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "version",

        "file_download",

        "created_at",

    )

    list_display_links = (

        "version",

    )

    search_fields = (

        "version",

        "description",

        "order__tracking_code",

    )

    autocomplete_fields = (

        "order",

    )

    readonly_fields = (

        "created_at",

        "file_download",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True

    @admin.display(description="دانلود فایل")

    def file_download(self, obj):

        return file_download(obj)


# ==========================================================
# INVOICE ADMIN
# ==========================================================

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "amount",

        "status",

        "due_date",

        "created_at",

    )

    list_display_links = (

        "order",

    )

    list_editable = (

        "status",

    )

    search_fields = (

        "order__tracking_code",

    )

    list_filter = (

        "status",

        "due_date",

        "created_at",

    )

    autocomplete_fields = (

        "order",

    )

    readonly_fields = (

        "created_at",

        "updated_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True

# ==========================================================
# CONTACT ADMIN
# ==========================================================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (

        "full_name",

        "subject",

        "phone",

        "email",

        "is_read",

        "created_at",

    )

    list_display_links = (

        "full_name",

    )

    list_editable = (

        "is_read",

    )

    search_fields = (

        "full_name",

        "subject",

        "phone",

        "email",

        "message",

    )

    list_filter = (

        "is_read",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True


# ==========================================================
# CAREER ADMIN
# ==========================================================

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):

    list_display = (

        "title",

        "salary",

        "active",

        "created_at",

    )

    list_display_links = (

        "title",

    )

    list_editable = (

        "active",

    )

    search_fields = (

        "title",

        "description",

        "requirements",

    )

    list_filter = (

        "active",

        "created_at",

    )

    readonly_fields = (

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 25

    save_on_top = True

    prepopulated_fields = {

        "slug": ("title",)

    }


# ==========================================================
# JOB APPLICATION ADMIN
# ==========================================================

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (

        "full_name",

        "career",

        "phone",

        "email",

        "created_at",

    )

    list_display_links = (

        "full_name",

    )

    search_fields = (

        "full_name",

        "phone",

        "email",

        "career__title",

    )

    list_filter = (

        "career",

        "created_at",

    )

    autocomplete_fields = (

        "career",

    )

    readonly_fields = (

        "created_at",

    )

    ordering = (

        "-created_at",

    )

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True

# ==========================================================
# ADMIN ACTIONS
# ==========================================================

@admin.action(description="✔ تغییر وضعیت به تکمیل شده")
def make_completed(modeladmin, request, queryset):

    queryset.update(

        status="completed"

    )


@admin.action(description="⏳ تغییر وضعیت به در حال انجام")
def make_processing(modeladmin, request, queryset):

    queryset.update(

        status="processing"

    )


@admin.action(description="❌ تغییر وضعیت به لغو شده")
def make_cancelled(modeladmin, request, queryset):

    queryset.update(

        status="cancelled"

    )


@admin.action(description="📌 تغییر وضعیت به در انتظار")
def make_pending(modeladmin, request, queryset):

    queryset.update(

        status="pending"

    )


# ==========================================================
# ADD ACTIONS TO ORDER ADMIN
# ==========================================================

OrderAdmin.actions = (

    make_completed,

    make_processing,

    make_cancelled,

    make_pending,

)


# ==========================================================
# OPTIMIZED QUERYSETS
# ==========================================================

def order_queryset(self, request):

    return (

        super(OrderAdmin, self)

        .get_queryset(request)

        .select_related(

            "user",

            "service",

        )

    )


OrderAdmin.get_queryset = order_queryset


# ==========================================================
# ADMIN SITE OPTIONS
# ==========================================================

admin.site.site_title = "Nexora Admin"

admin.site.site_header = "Nexora Web Management"

admin.site.index_title = "Control Panel"

admin.site.empty_value_display = "-"

# ==========================================================
# EXTRA ADMIN FEATURES
# ==========================================================

@admin.display(description="تعداد سفارش‌ها")
def orders_count(obj):

    return obj.order_set.count()


@admin.display(description="تعداد نمونه‌کارها")
def portfolios_count(obj):

    return obj.portfolio_set.count()


@admin.display(description="وضعیت فاکتور")
def invoice_status(obj):

    try:

        return obj.invoice.get_status_display()

    except Exception:

        return "-"


@admin.display(description="تعداد تیکت‌ها")
def tickets_count(obj):

    return obj.tickets.count()


# ==========================================================
# EXTRA CONFIG
# ==========================================================

OrderAdmin.list_select_related = (

    "user",

    "service",

)

PortfolioAdmin.list_select_related = (

    "service",

)

InvoiceAdmin.list_select_related = (

    "order",

)

TicketAdmin.list_select_related = (

    "order",

    "sender",

)

TaskAdmin.list_select_related = (

    "order",

)

ProgressAdmin.list_select_related = (

    "order",

)

TimelineAdmin.list_select_related = (

    "order",

)

VersionAdmin.list_select_related = (

    "order",

)

JobApplicationAdmin.list_select_related = (

    "career",

)


# ==========================================================
# SAVE BUTTONS
# ==========================================================

ServiceAdmin.save_as = True

PortfolioAdmin.save_as = True

OrderAdmin.save_as = True

CareerAdmin.save_as = True


# ==========================================================
# SEARCH HELP
# ==========================================================

ServiceAdmin.search_help_text = "عنوان سرویس"

PortfolioAdmin.search_help_text = "عنوان پروژه یا نام مشتری"

OrderAdmin.search_help_text = "کد رهگیری، نام مشتری یا ایمیل"

TicketAdmin.search_help_text = "کد سفارش یا پیام"

CareerAdmin.search_help_text = "عنوان موقعیت شغلی"

JobApplicationAdmin.search_help_text = "نام متقاضی یا ایمیل"

InvoiceAdmin.search_help_text = "کد رهگیری سفارش"

# ==========================================================
# FINAL ADMIN CONFIG
# ==========================================================

admin.site.enable_nav_sidebar = True

admin.site.site_title = "Nexora Administration"

admin.site.site_header = "Nexora Control Panel"

admin.site.index_title = "Dashboard"


# ==========================================================
# GLOBAL ADMIN SETTINGS
# ==========================================================

for model_admin in (

    ServiceAdmin,

    PortfolioAdmin,

    OrderAdmin,

    TicketAdmin,

    ProgressAdmin,

    TimelineAdmin,

    TaskAdmin,

    VersionAdmin,

    InvoiceAdmin,

    ContactAdmin,

    CareerAdmin,

    JobApplicationAdmin,

):

    model_admin.save_on_top = True

    model_admin.list_per_page = 25

    model_admin.show_facets = admin.ShowFacets.ALWAYS


# ==========================================================
# ADMIN LOG CONFIG
# ==========================================================

admin.site.empty_value_display = "-"


# ==========================================================
# END OF FILE
# ==========================================================
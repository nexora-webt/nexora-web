# ==========================================================
# IMPORTS
# ==========================================================

from django.contrib import admin

from django.utils.html import format_html

from django.db.models import Count

from .models import (
    Category,
    Service,
    Portfolio,
    PortfolioImage,
    Order,
    OrderFile,
    Payment,
    Invoice,
    ContactMessage,
    SiteSetting,
    FAQ,
    Team,
    Review,
    BlogCategory,
    Tag,
    Blog,
)



# ==========================================================
# ADMIN HELPERS
# ==========================================================


def image_preview(obj, field="image"):

    image = getattr(
        obj,
        field,
        None,
    )


    if image:

        return format_html(

            '<img src="{}" width="90" '
            'style="border-radius:10px;'
            'border:1px solid #ddd;">',

            image.url,

        )


    return "-"



image_preview.short_description = "پیش‌نمایش"



def status_badge(obj):

    colors = {

        "pending": "#ffc107",

        "processing": "#0dcaf0",

        "completed": "#198754",

        "cancelled": "#dc3545",

        "paid": "#198754",

        "failed": "#dc3545",

    }


    status = getattr(
        obj,
        "status",
        "",
    )


    return format_html(

        '<span style="background:{};'
        'color:white;'
        'padding:5px 12px;'
        'border-radius:15px;">'
        '{}'
        '</span>',

        colors.get(
            status,
            "#6c757d",
        ),

        status,

    )



status_badge.short_description = "وضعیت"



# ==========================================================
# ADMIN SITE CONFIG
# ==========================================================


admin.site.site_title = "Nexora Administration"

admin.site.site_header = "Nexora Control Panel"

admin.site.index_title = "Dashboard"

admin.site.empty_value_display = "-"

# ==========================================================
# CATEGORY ADMIN
# ==========================================================


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):


    list_display = (

        "title",

        "slug",

        "service_count",

        "is_active",

        "created_at",

    )


    list_display_links = (

        "title",

    )


    list_editable = (

        "is_active",

    )


    search_fields = (

        "title",

        "description",

    )


    list_filter = (

        "is_active",

        "created_at",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    prepopulated_fields = {

        "slug": (

            "title",

        )

    }


    ordering = (

        "title",

    )


    list_per_page = 25


    save_on_top = True



    def get_queryset(self, request):

        queryset = super().get_queryset(request)


        return queryset.annotate(

            total_services=Count(
                "services"
            )

        )



    @admin.display(

        description="تعداد سرویس‌ها",

        ordering="total_services",

    )

    def service_count(self, obj):

        return obj.total_services

# ==========================================================
# SERVICE ADMIN
# ==========================================================


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):


    list_display = (

        "title",

        "category",

        "base_price",

        "portfolio_count",

        "is_active",

        "created_at",

    )


    list_display_links = (

        "title",

    )


    list_editable = (

        "is_active",

    )


    search_fields = (

        "title",

        "description",

        "slug",

    )


    list_filter = (

        "category",

        "is_active",

        "created_at",

    )


    autocomplete_fields = (

        "category",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    prepopulated_fields = {

        "slug": (

            "title",

        )

    }


    ordering = (

        "-created_at",

    )


    list_per_page = 25


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات اصلی",

            {

                "fields": (

                    "title",

                    "slug",

                    "category",

                    "description",

                )

            },

        ),


        (

            "تنظیمات سرویس",

            {

                "fields": (

                    "base_price",

                    "icon",

                    "is_active",

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

        description="نمونه‌کارها",

        ordering="total_portfolios",
    )

    def portfolio_count(self, obj):

        return "-"

# ==========================================================
# PORTFOLIO IMAGE INLINE
# ==========================================================


class PortfolioImageInline(admin.TabularInline):

    model = PortfolioImage

    extra = 1


    fields = (

        "image",

        "preview",

        "alt_text",

        "order",

    )


    readonly_fields = (

        "preview",

    )


    ordering = (

        "order",

    )


    @admin.display(
        description="پیش‌نمایش"
    )
    def preview(self, obj):

        return image_preview(
            obj,
            "image",
        )



# ==========================================================
# PORTFOLIO ADMIN
# ==========================================================

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):

    list_display = (
        "preview",
        "title",
        "category",
        "client_name",
        "is_featured",
        "views",
        "created_at",
        "service",
        "project_status",
        "is_public",
    )

    list_display_links = (

        "preview",
        "title",
    )

    list_editable = (

        "is_featured",
    )

    search_fields = (
        "title",
        "description",
        "client_name",
        "technologies",
        "service",
        "slug",
    )

    list_filter = (

        "category",

        "is_featured",

        "is_active",

        "created_at",
    )

    autocomplete_fields = (

        "category",
        "service",
    )

    readonly_fields = (

        "preview",

        "views",

        "created_at",

        "updated_at",

    )


    prepopulated_fields = {

        "slug": (

            "title",

        )

    }


    ordering = (

        "-created_at",

    )


    list_per_page = 25


    save_on_top = True


    inlines = (

        PortfolioImageInline,

    )


    fieldsets = (

        (
            "اطلاعات پروژه",
            {
                "fields": (
                    "title",
                    "slug",
                    "service",
                    "category",
                    "description",
                    "technologies",
                )
            },
        ),

        (
            "اطلاعات مشتری",
            {
                "fields": (
                    "client_name",
                    "client_company",
                )
            },
        ),


        (
            "اطلاعات آنلاین پروژه",
            {
                "fields": (
                    "live_demo_url",
                    "github_url",
                    "completion_date",
                    "project_duration",
                    "project_status",
                )
            },
        ),


        (
            "تصویر اصلی",
            {
                "fields": (
                    "cover_image",
                    "preview",
                )
            },
        ),


        (
            "تنظیمات نمایش",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                    "is_public",
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
                    "updated_at",
                )
            },
        ),

    )

    @admin.display(
        description="تصویر"
    )
    def preview(self, obj):

        return image_preview(
            obj,
            "cover_image",
        )



    def get_queryset(self, request):

        return super().get_queryset(
            request
        ).select_related(
            "category",
            "service",
        )

# ==========================================================
# ORDER FILE INLINE
# ==========================================================


class OrderFileInline(admin.TabularInline):

    model = OrderFile

    extra = 0


    fields = (

        "file",

        "description",

        "created_at",
    )

    readonly_fields = (

        "created_at",
    )

# ==========================================================
# ORDER ADMIN
# ==========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        "tracking_code",

        "name",

        "phone",

        "service",

        "status_badge",

        "estimated_price",

        "created_at",

        "status",
    )

    list_display_links = (

        "tracking_code",

        "name",
    )

    list_editable = (

        "status",
    )

    search_fields = (

        "tracking_code",

        "name",

        "phone",

        "email",

        "description",
    )

    list_filter = (

        "status",

        "service",

        "created_at",
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


    list_per_page = 30


    save_on_top = True


    inlines = (

        OrderFileInline,

    )



    actions = (

        "mark_processing",

        "mark_completed",

        "mark_cancelled",

        "mark_pending",

    )

    fieldsets = (

        (

            "اطلاعات مشتری",

            {

                "fields": (

                    "user",

                    "name",

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

            "مدیریت سفارش",

            {
                "fields": (

                    "status",

                    "estimated_price",

                    "tracking_code",

                    "developers",
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

                )

            },

        ),

    )



    @admin.display(
        description="وضعیت"
    )
    def status_badge(self, obj):

        return status_badge(obj)



    @admin.action(
        description="⏳ تغییر به در حال انجام"
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
        description="✔ تغییر به تکمیل شده"
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
        description="❌ تغییر به لغو شده"
    )
    def mark_cancelled(
        self,
        request,
        queryset,
    ):

        queryset.update(
            status="cancelled"
        )



    @admin.action(
        description="🕒 تغییر به در انتظار"
    )
    def mark_pending(
        self,
        request,
        queryset,
    ):

        queryset.update(
            status="pending"
        )



    def get_queryset(self, request):

        return super().get_queryset(
            request
        ).select_related(
            "user",
            "service",
        )

# ==========================================================
# PAYMENT ADMIN
# ==========================================================


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):


    list_display = (

        "order",

        "amount",

        "payment_method",

        "status_badge",

        "transaction_id",

        "created_at",

    )


    list_display_links = (

        "order",

    )


    search_fields = (

        "order__tracking_code",

        "transaction_id",

    )


    list_filter = (

        "payment_method",

        "status",

        "created_at",

    )


    autocomplete_fields = (

        "order",

    )


    readonly_fields = (

        "transaction_id",

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 30


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات پرداخت",

            {

                "fields": (

                    "order",

                    "amount",

                    "payment_method",

                    "status",

                )

            },

        ),


        (

            "اطلاعات تراکنش",

            {

                "fields": (

                    "transaction_id",

                    "gateway_response",

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

                )

            },

        ),

    )



    @admin.display(
        description="وضعیت"
    )
    def status_badge(self, obj):

        return status_badge(obj)



    def get_queryset(self, request):

        return super().get_queryset(
            request
        ).select_related(
            "order",
        )

# ==========================================================
# INVOICE ADMIN
# ==========================================================


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):


    list_display = (

        "invoice_number",

        "order",

        "amount",

        "status_badge",

        "created_at",

        "status",
    )


    list_display_links = (

        "invoice_number",

        "order",

    )


    list_editable = (

        "status",

    )


    search_fields = (

        "invoice_number",

        "order__tracking_code",

        "order__name",

    )


    list_filter = (

        "status",

        "created_at",

    )


    autocomplete_fields = (

        "order",

    )


    readonly_fields = (

        "invoice_number",

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 30


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات فاکتور",

            {

                "fields": (

                    "order",

                    "invoice_number",

                    "amount",

                    "status",

                )

            },

        ),


        (

            "توضیحات",

            {

                "fields": (

                    "description",

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
    def status_badge(self, obj):

        return status_badge(obj)



    def get_queryset(self, request):

        return super().get_queryset(
            request
        ).select_related(
            "order",
        )

# ==========================================================
# CONTACT MESSAGE ADMIN
# ==========================================================


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):


    list_display = (

        "name",

        "email",

        "phone",

        "subject",

        "is_read",

        "created_at",

    )


    list_display_links = (

        "name",

    )


    list_editable = (

        "is_read",

    )


    search_fields = (

        "name",

        "email",

        "phone",

        "subject",

        "message",

    )


    list_filter = (

        "is_read",

        "created_at",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 30


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات فرستنده",

            {

                "fields": (

                    "name",

                    "email",

                    "phone",

                )

            },

        ),


        (

            "پیام",

            {

                "fields": (

                    "subject",

                    "message",

                )

            },

        ),


        (

            "مدیریت",

            {

                "fields": (

                    "is_read",

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

                )

            },

        ),

    )





# ==========================================================
# SITE SETTING ADMIN
# ==========================================================


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):


    list_display = (

        "site_name",

        "phone",

        "email",

        "updated_at",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    fieldsets = (

        (

            "اطلاعات برند",

            {

                "fields": (

                    "site_name",

                    "logo",

                    "description",

                )

            },

        ),


        (

            "ارتباطات",

            {

                "fields": (

                    "email",

                    "phone",

                    "address",

                )

            },

        ),


        (

            "شبکه‌های اجتماعی",

            {

                "fields": (

                    "instagram",

                    "telegram",

                    "linkedin",

                )

            },

        ),


        (

            "سیستم",

            {

                "classes": (

                    "collapse",

                ),

                "fields": (

                    "created_at",

                    "updated_at",

                )

            },

        ),

    )





# ==========================================================
# FAQ ADMIN
# ==========================================================


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):


    list_display = (

        "question",

        "order",

        "is_active",

        "created_at",

    )


    list_display_links = (

        "question",

    )


    list_editable = (

        "order",

        "is_active",

    )


    search_fields = (

        "question",

        "answer",

    )


    list_filter = (

        "is_active",

        "created_at",

    )


    ordering = (

        "order",

        "-created_at",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    list_per_page = 30


    save_on_top = True

# ==========================================================
# TEAM ADMIN
# ==========================================================


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):


    list_display = (

        "preview",

        "name",

        "role",

        "is_active",

        "order",

        "created_at",

    )


    list_display_links = (

        "preview",

        "name",

    )


    list_editable = (

        "is_active",

        "order",

    )


    search_fields = (

        "name",

        "role",

        "bio",

    )


    list_filter = (

        "is_active",

        "created_at",

    )


    readonly_fields = (

        "preview",

        "created_at",

        "updated_at",

    )


    ordering = (

        "order",

        "-created_at",

    )


    list_per_page = 25


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات عضو تیم",

            {

                "fields": (

                    "name",

                    "role",

                    "bio",

                )

            },

        ),


        (

            "تصویر",

            {

                "fields": (

                    "avatar",

                    "preview",

                )

            },

        ),


        (

            "تنظیمات",

            {

                "fields": (

                    "order",

                    "is_active",

                )

            },

        ),


        (

            "سیستم",

            {

                "classes": (

                    "collapse",

                ),

                "fields": (

                    "created_at",

                    "updated_at",

                )

            },

        ),

    )



    @admin.display(
        description="تصویر"
    )
    def preview(self, obj):

        return image_preview(
            obj,
            "avatar",
        )





# ==========================================================
# REVIEW ADMIN
# ==========================================================


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):


    list_display = (

        "name",

        "company",

        "rating",

        "is_active",

        "created_at",

    )


    list_display_links = (

        "name",

    )


    list_editable = (

        "rating",

        "is_active",

    )


    search_fields = (

        "name",

        "company",

        "message",

    )


    list_filter = (

        "rating",

        "is_active",

        "created_at",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 30


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات مشتری",

            {

                "fields": (

                    "name",

                    "company",

                    "message",

                )

            },

        ),


        (

            "امتیاز",

            {

                "fields": (

                    "rating",

                    "is_active",

                )

            },

        ),


        (

            "سیستم",

            {

                "classes": (

                    "collapse",

                ),

                "fields": (

                    "created_at",

                    "updated_at",

                )

            },

        ),

    )

# ==========================================================
# BLOG CATEGORY ADMIN
# ==========================================================


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):


    list_display = (

        "title",

        "slug",

        "is_active",

        "created_at",

    )


    list_display_links = (

        "title",

    )


    list_editable = (

        "is_active",

    )


    search_fields = (

        "title",

        "description",

    )


    list_filter = (

        "is_active",

        "created_at",

    )


    prepopulated_fields = {

        "slug": (

            "title",

        )

    }


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 25


    save_on_top = True





# ==========================================================
# TAG ADMIN
# ==========================================================


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):


    list_display = (

        "name",

        "slug",

        "created_at",

    )


    list_display_links = (

        "name",

    )


    search_fields = (

        "name",

    )


    prepopulated_fields = {

        "slug": (

            "name",

        )

    }


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    ordering = (

        "name",

    )





# ==========================================================
# BLOG ADMIN
# ==========================================================


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):


    list_display = (

        "preview",

        "title",

        "category",

        "author",

        "views",

        "is_published",

        "created_at",

    )


    list_display_links = (

        "preview",

        "title",

    )


    list_editable = (

        "is_published",

    )


    search_fields = (

        "title",

        "content",

        "slug",

    )


    list_filter = (

        "category",

        "is_published",

        "created_at",

    )


    autocomplete_fields = (

        "category",

        "author",

    )


    filter_horizontal = (

        "tags",

    )


    readonly_fields = (

        "preview",

        "views",

        "created_at",

        "updated_at",

    )


    prepopulated_fields = {

        "slug": (

            "title",

        )

    }


    ordering = (

        "-created_at",

    )


    list_per_page = 25


    save_on_top = True



    fieldsets = (

        (

            "اطلاعات مقاله",

            {

                "fields": (

                    "title",

                    "slug",

                    "category",

                    "author",

                    "content",

                )

            },

        ),


        (

            "رسانه",

            {

                "fields": (

                    "image",

                    "preview",

                )

            },

        ),


        (

            "تنظیمات",

            {

                "fields": (

                    "tags",

                    "is_published",

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

                    "updated_at",

                )

            },

        ),

    )



    @admin.display(
        description="تصویر"
    )
    def preview(self, obj):

        return image_preview(
            obj,
            "image",
        )



    def get_queryset(self, request):

        return super().get_queryset(
            request
        ).select_related(
            "category",
            "author",
        )





# ==========================================================
# GLOBAL ADMIN SETTINGS
# ==========================================================


for model_admin in (

    CategoryAdmin,

    ServiceAdmin,

    PortfolioAdmin,

    OrderAdmin,

    PaymentAdmin,

    InvoiceAdmin,

    ContactMessageAdmin,

    SiteSettingAdmin,

    FAQAdmin,

    TeamAdmin,

    ReviewAdmin,

    BlogCategoryAdmin,

    TagAdmin,

    BlogAdmin,

):

    model_admin.save_on_top = True

    model_admin.list_per_page = 25



# ==========================================================
# FINAL ADMIN CONFIG
# ==========================================================


admin.site.enable_nav_sidebar = True

admin.site.empty_value_display = "-"


# ==========================================================
# END OF FILE
# ==========================================================
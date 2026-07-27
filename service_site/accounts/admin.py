# ==========================================================
# IMPORTS
# ==========================================================

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    UserProfile,
    Department,
    Employee,
)



# ==========================================================
# USER PROFILE ADMIN
# ==========================================================


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):


    list_display = (

        "avatar_preview",

        "user",

        "role",

        "phone",

        "created_at",

    )


    list_display_links = (

        "user",

    )


    search_fields = (

        "user__username",

        "user__email",

        "phone",

        "bio",

    )


    list_filter = (

        "role",

        "created_at",

    )


    readonly_fields = (

        "avatar_preview",

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 30



    @admin.display(

        description="تصویر"

    )

    def avatar_preview(self, obj):


        if obj.avatar:


            return format_html(

                '<img src="{}" width="60" '
                'style="border-radius:50%;">',

                obj.avatar.url,

            )


        return "-"





# ==========================================================
# DEPARTMENT ADMIN
# ==========================================================


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):


    list_display = (

        "name",

        "department_type",

        "manager",

        "order",

        "is_active",

    )


    list_display_links = (

        "name",

    )


    search_fields = (

        "name",

        "description",

    )


    list_filter = (

        "department_type",

        "is_active",

    )


    autocomplete_fields = (

        "manager",

    )


    list_editable = (

        "order",

        "is_active",

    )


    ordering = (

        "order",

        "name",

    )





# ==========================================================
# EMPLOYEE ADMIN
# ==========================================================


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):


    list_display = (

        "user",

        "department",

        "position",

        "is_available",

        "created_at",

    )


    list_display_links = (

        "user",

    )


    search_fields = (

        "user__username",

        "user__email",

        "position",

        "skills",

    )


    list_filter = (

        "department",

        "is_available",

        "created_at",

    )


    autocomplete_fields = (

        "user",

        "department",

    )


    readonly_fields = (

        "created_at",

        "updated_at",

    )


    ordering = (

        "-created_at",

    )


    list_per_page = 30



# ==========================================================
# GLOBAL ADMIN SETTINGS
# ==========================================================


admin.site.site_title = "Nexora Administration"

admin.site.site_header = "Nexora Web Control Panel"

admin.site.index_title = "Dashboard"
from django.contrib import admin
from .models import UserProfile
from .models import Department
from .models import Employee


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (

        "user",

        "department",

        "job_title",

        "active",

    )

    list_filter = (

        "department",

        "active",

    )
from django.contrib import admin
from .models import Service, Order, Portfolio

# ====================== خدمات ======================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'base_price', 'icon']
    search_fields = ['title', 'description']
    list_filter = ['base_price']
    ordering = ['title']


# ====================== نمونه کارها ======================
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'created_at']
    list_filter = ['service']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


# ====================== سفارشات ======================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service', 'estimated_price', 'status', 'created_at']
    list_filter = ['status', 'service']
    search_fields = ['name', 'phone', 'description']
    readonly_fields = ['estimated_price', 'created_at']
    ordering = ['-created_at']
    
    # نمایش زیبا در جزئیات
    fieldsets = [
        ('اطلاعات مشتری', {'fields': ['name', 'phone', 'email']}),
        ('جزئیات سفارش', {'fields': ['service', 'description', 'estimated_price']}),
        ('وضعیت', {'fields': ['status']}),
    ]
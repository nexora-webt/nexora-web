"""
URL configuration for service_site project.
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import register_converter
from core.converters import UnicodeSlugConverter

register_converter(UnicodeSlugConverter, "uslug")

urlpatterns = [

    # Django Language
    path(
        "i18n/",
        include("django.conf.urls.i18n"),
    ),

    # Django Admin
    path(
        "control-panel-x9K2aP7/",
        admin.site.urls,
    ),

    # Accounts
    path(
        "accounts/",
        include("accounts.urls"),
    ),

]

# Main Website
urlpatterns += i18n_patterns(

    path(
        "",
        include("core.urls"),
    ),

)

# Media & Static (Development Only)
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
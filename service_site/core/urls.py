from django.urls import path

from . import views


app_name = "core"


urlpatterns = [

    # ==========================
    # Home
    # ==========================

    path(
        "",
        views.home,
        name="home",
    ),

    # ==========================
    # About
    # ==========================

    path(
        "about/",
        views.about,
        name="about",
    ),

    path(
    "contact/",
    views.contact,
    name="contact",
    ),

    # ==========================
    # Success
    # ==========================

    path(
        "success/",
        views.success,
        name="success",
    ),

    # ==========================
    # Careers
    # ==========================

    path(
        "careers/",
        views.careers,
        name="careers",
    ),

    # ==========================
    # Services
    # ==========================

    path(
    "services/<uslug:slug>/",
    views.service_detail,
    name="service_detail",
    ),
    # ==========================
    # Portfolio
    # ==========================

    path(
        "portfolio/<uslug:slug>/",
        views.portfolio_detail,
        name="portfolio_detail",
    ),

    # ==========================
    # Tracking
    # ==========================

    path(
        "tracking/",
        views.tracking,
        name="tracking",
    ),

    # ==========================
    # Dashboard
    # ==========================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # ==========================
    # Order Detail
    # ==========================

    path(
        "order/<str:tracking_code>/",
        views.order_detail,
        name="order_detail",
    ),

    # ==========================
    # Invoice PDF
    # ==========================

    path(
        "invoice/<str:tracking_code>/",
        views.invoice_pdf,
        name="invoice_pdf",
    ),

]
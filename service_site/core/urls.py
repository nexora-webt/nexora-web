from django.urls import path

from . import views

from django.conf.urls.i18n import i18n_patterns

app_name = "core"



urlpatterns = [

    # ==========================================================
    # HOME
    # ==========================================================

    path(
        "",
        views.home,
        name="home",
    ),


    # ==========================================================
    # STATIC PAGES
    # ==========================================================

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


    path(
        "success/",
        views.success,
        name="success",
    ),



    # ==========================================================
    # SERVICES
    # ==========================================================

    path(
        "services/<slug:slug>/",
        views.service_detail,
        name="service_detail",
    ),



    # ==========================================================
    # PORTFOLIO
    # ==========================================================

    path(
        "portfolio/<slug:slug>/",
        views.portfolio_detail,
        name="portfolio_detail",
    ),



    # ==========================================================
    # ORDER TRACKING
    # ==========================================================

    path(
        "tracking/",
        views.tracking,
        name="tracking",
    ),



    # ==========================================================
    # USER DASHBOARD
    # ==========================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),



    # ==========================================================
    # ORDER DETAIL
    # ==========================================================

    path(
        "order/<str:tracking_code>/",
        views.order_detail,
        name="order_detail",
    ),



    # ==========================================================
    # INVOICE PDF
    # ==========================================================

    path(
        "invoice/<str:tracking_code>/",
        views.invoice_pdf,
        name="invoice_pdf",
    ),

]

urlpatterns += i18n_patterns(
    path("", views.home, name="home"),
)
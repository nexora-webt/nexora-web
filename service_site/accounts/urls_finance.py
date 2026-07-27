from django.urls import path

from . import views


urlpatterns = [

    path(
        "invoice/<str:tracking_code>/",
        views.invoice_detail,
        name="invoice_detail",
    ),



    path(
        "invoice/<str:tracking_code>/download/",
        views.download_invoice,
        name="download_invoice",
    ),



    path(
        "payments/",
        views.payment_history,
        name="payment_history",
    ),

]
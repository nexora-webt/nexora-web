from django.urls import path, include


app_name = "accounts"


urlpatterns = [

    path(
        "",
        include("accounts.urls_auth")
    ),


    path(
        "",
        include("accounts.urls_profile")
    ),


    path(
        "",
        include("accounts.urls_dashboard")
    ),


    path(
        "",
        include("accounts.urls_orders")
    ),


    path(
        "",
        include("accounts.urls_support")
    ),


    path(
        "",
        include("accounts.urls_finance")
    ),

]
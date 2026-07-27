from django.urls import path

from . import views


urlpatterns = [

    path(
        "register/",
        views.register_view,
        name="register",
    ),


    path(
        "login/",
        views.login_view,
        name="login",
    ),


    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),



    path(
        "verify/<uidb64>/<token>/",
        views.verify_email,
        name="verify_email",
    ),


    path(
        "verify/resend/",
        views.resend_email_verification,
        name="resend_email_verification",
    ),



    path(
        "password/reset/",
        views.password_reset_request,
        name="password_reset",
    ),


    path(
        "password/reset/complete/",
        views.password_reset_complete,
        name="password_reset_complete",
    ),


    path(
        "password/change/",
        views.change_password,
        name="change_password",
    ),

]
from django.urls import path

from . import views


urlpatterns = [

    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),


    path(
        "profile/detail/",
        views.profile_detail,
        name="profile_detail",
    ),


    path(
        "profile/avatar/delete/",
        views.delete_avatar,
        name="delete_avatar",
    ),



    path(
        "settings/",
        views.account_settings,
        name="settings",
    ),



    path(
        "security/",
        views.security_center,
        name="security_center",
    ),

]
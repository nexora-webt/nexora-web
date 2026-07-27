from django.urls import path

from . import views


urlpatterns = [

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),



    path(
        "notifications/",
        views.notifications_view,
        name="notifications",
    ),


    path(
        "notifications/read/<int:notification_id>/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),


    path(
        "notifications/read-all/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),



    path(
        "activity/",
        views.activity_history,
        name="activity_history",
    ),



    path(
        "dashboard/refresh/",
        views.refresh_dashboard_data,
        name="refresh_dashboard_data",
    ),

]
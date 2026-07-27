from django.urls import path

from . import views


urlpatterns = [

    path(
        "orders/<str:tracking_code>/ticket/create/",
        views.create_ticket,
        name="create_ticket",
    ),



    path(
        "tickets/",
        views.ticket_list,
        name="tickets",
    ),



    path(
        "tickets/<int:ticket_id>/",
        views.ticket_detail,
        name="ticket_detail",
    ),



    path(
        "tickets/<int:ticket_id>/reply/",
        views.reply_ticket,
        name="reply_ticket",
    ),

]
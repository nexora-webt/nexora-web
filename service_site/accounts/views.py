from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import (
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding import (
    force_bytes,
    force_str,
)
from django.core.exceptions import PermissionDenied
from django_ratelimit.decorators import ratelimit
from reportlab.pdfgen import canvas
from .forms import (
    RegisterForm,
    LoginForm,
    ProfileForm,
    ChangePasswordForm,
    TicketForm,
    TicketReplyForm,
    PasswordResetRequestForm,
)
from .models import (
    UserProfile,
    UserActivityLog,
    Notification,
)
from core.models import (
    Order,
    Ticket,
    Invoice,
)
def get_client_ip(request):
    x_forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if x_forwarded_for:

        ip = x_forwarded_for.split(",")[0]

    else:

        ip = request.META.get(
            "REMOTE_ADDR"
        )

    return ip

def create_activity_log(
    user,
    action,
    description="",
    request=None,
):

    ip_address = None

    user_agent = ""

    if request:

        ip_address = get_client_ip(
            request
        )

        user_agent = request.META.get(
            "HTTP_USER_AGENT",
            "",
        )

    return UserActivityLog.objects.create(

        user=user,

        action=action,

        description=description,

        ip_address=ip_address,

        user_agent=user_agent,

    )

def create_notification(
    user,
    title,
    message,
    notification_type="system",
):

    return Notification.objects.create(

        user=user,

        title=title,

        message=message,

        notification_type=notification_type,
    )

def user_has_permission(
    user,
    role,
):

    if not user.is_authenticated:

        return False

    profile = getattr(
        user,
        "profile",
        None,
    )

    if not profile:

        return False

    return profile.role == role

def require_role(
    user,
    roles,
):

    if not user.is_authenticated:

        raise PermissionDenied

    profile = getattr(
        user,
        "profile",
        None,
    )

    if not profile:

        raise PermissionDenied

    if profile.role not in roles:

        raise PermissionDenied

@ratelimit(
    key="ip",
    rate="3/m",
    method="POST",
    block=True,
)
def register_view(request):

    if request.user.is_authenticated:

        return redirect(
            "accounts:dashboard"
        )


    form = RegisterForm(
        request.POST or None
    )


    if form.is_valid():


        user = form.save()


        user.email = form.cleaned_data.get(
            "email"
        )

        user.save()



        UserProfile.objects.get_or_create(
            user=user
        )



        create_activity_log(

            user,

            "register",

            "ثبت نام کاربر جدید",

            request,

        )



        create_notification(

            user,

            "خوش آمدید",

            "حساب شما در Nexora Web ساخته شد.",

            "system",

        )



        login(
            request,
            user,
        )



        messages.success(

            request,

            "ثبت نام با موفقیت انجام شد."

        )



        return redirect(

            "accounts:dashboard"

        )



    return render(

        request,

        "accounts/register.html",

        {

            "form": form,

        },

    )





@ratelimit(
    key="ip",
    rate="10/m",
    method="POST",
    block=True,
)
def login_view(request):


    if request.user.is_authenticated:


        return redirect(

            "accounts:dashboard"

        )



    form = LoginForm(

        request,

        data=request.POST or None,

    )



    if form.is_valid():


        user = form.get_user()



        login(

            request,

            user,

        )



        create_activity_log(

            user,

            "login",

            "ورود موفق به حساب کاربری",

            request,

        )



        create_notification(

            user,

            "ورود جدید",

            "ورود جدید به حساب Nexora Web انجام شد.",

            "security",

        )



        messages.success(

            request,

            "خوش آمدید."

        )



        return redirect(

            "accounts:dashboard"

        )



    return render(

        request,

        "accounts/login.html",

        {

            "form": form,

        },

    )





@login_required
def logout_view(request):


    create_activity_log(

        request.user,

        "logout",

        "خروج از حساب کاربری",

        request,

    )



    logout(

        request

    )



    messages.success(

        request,

        "با موفقیت خارج شدید."

    )



    return redirect(

        "core:home"

    )

from django.core.mail import send_mail

from django.conf import settings

from django.contrib.auth.tokens import default_token_generator

from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)

from django.utils.encoding import (
    force_bytes,
    force_str,
)



def send_email_verification(
    user,
):


    uid = urlsafe_base64_encode(

        force_bytes(
            user.pk
        )

    )


    token = default_token_generator.make_token(

        user

    )


    verification_url = (

        f"/accounts/verify/{uid}/{token}/"

    )


    send_mail(

        "تأیید ایمیل Nexora Web",

        f"برای فعال‌سازی حساب خود وارد شوید:\n{verification_url}",

        settings.DEFAULT_FROM_EMAIL,

        [
            user.email
        ],

        fail_silently=False,

    )





@login_required
def resend_email_verification(request):


    user = request.user



    if user.is_active:


        messages.info(

            request,

            "حساب شما قبلاً فعال شده است."

        )


        return redirect(

            "accounts:dashboard"

        )



    send_email_verification(

        user

    )



    create_activity_log(

        user,

        "email_verification_request",

        "درخواست ارسال مجدد تأیید ایمیل",

        request,

    )



    messages.success(

        request,

        "لینک تأیید ایمیل ارسال شد."

    )



    return redirect(

        "accounts:dashboard"

    )





def verify_email(
    request,
    uidb64,
    token,
):


    try:


        uid = force_str(

            urlsafe_base64_decode(

                uidb64

            )

        )


        user = User.objects.get(

            pk=uid

        )


    except (

        TypeError,

        ValueError,

        OverflowError,

        User.DoesNotExist,

    ):


        user = None





    if user and default_token_generator.check_token(

        user,

        token,

    ):



        user.is_active = True


        user.save()



        UserProfile.objects.get_or_create(

            user=user

        )



        create_activity_log(

            user,

            "email_verified",

            "ایمیل کاربر تأیید شد.",

            request,

        )



        create_notification(

            user,

            "تأیید ایمیل",

            "ایمیل شما با موفقیت تأیید شد.",

            "security",

        )



        messages.success(

            request,

            "ایمیل شما تأیید شد."

        )



        return redirect(

            "accounts:login"

        )



    messages.error(

        request,

        "لینک تأیید ایمیل معتبر نیست."

    )


    return redirect(

        "core:home"

    )

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
)



def password_reset_request(request):


    if request.method == "POST":


        form = PasswordResetRequestForm(

            request.POST

        )


        if form.is_valid():


            email = form.cleaned_data.get(

                "email"

            )


            user = User.objects.filter(

                email=email

            ).first()



            if user:


                create_activity_log(

                    user,

                    "password_reset_request",

                    "درخواست بازیابی رمز عبور",

                    request,

                )



                create_notification(

                    user,

                    "بازیابی رمز عبور",

                    "درخواست بازیابی رمز عبور ثبت شد.",

                    "security",

                )



            messages.success(

                request,

                "اگر ایمیل وجود داشته باشد، لینک بازیابی ارسال می‌شود."

            )



            return redirect(

                "accounts:login"

            )


    else:


        form = PasswordResetRequestForm()



    return render(

        request,

        "accounts/password_reset.html",

        {

            "form": form,

        },

    )





@login_required
@ratelimit(
    key="user",
    rate="5/h",
    method="POST",
    block=True,
)
def change_password(request):


    if request.method == "POST":


        form = ChangePasswordForm(

            request.user,

            request.POST,

        )



        if form.is_valid():


            user = form.save()



            update_session_auth_hash(

                request,

                user,

            )



            create_activity_log(

                user,

                "password_change",

                "رمز عبور تغییر کرد.",

                request,

            )



            create_notification(

                user,

                "تغییر رمز عبور",

                "رمز عبور حساب شما تغییر کرد.",

                "security",

            )



            messages.success(

                request,

                "رمز عبور با موفقیت تغییر کرد."

            )



            return redirect(

                "accounts:profile"

            )



    else:


        form = ChangePasswordForm(

            request.user

        )



    return render(

        request,

        "accounts/change_password.html",

        {

            "form": form,

        },

    )





def password_reset_complete(request):


    messages.success(

        request,

        "رمز عبور شما با موفقیت تغییر کرد."

    )


    return redirect(

        "accounts:login"

    )

@login_required
def profile_view(request):


    profile, created = UserProfile.objects.get_or_create(

        user=request.user

    )


    form = ProfileForm(

        request.POST or None,

        request.FILES or None,

        instance=profile,

    )


    if form.is_valid():


        form.save()



        create_activity_log(

            request.user,

            "profile_update",

            "پروفایل کاربر بروزرسانی شد.",

            request,

        )



        create_notification(

            request.user,

            "بروزرسانی پروفایل",

            "اطلاعات پروفایل شما تغییر کرد.",

            "system",

        )



        messages.success(

            request,

            "پروفایل با موفقیت بروزرسانی شد."

        )



        return redirect(

            "accounts:profile"

        )



    return render(

        request,

        "accounts/profile.html",

        {

            "form": form,

            "profile": profile,

        },

    )





@login_required
def profile_detail(request):


    profile = get_object_or_404(

        UserProfile,

        user=request.user,

    )



    return render(

        request,

        "accounts/profile_detail.html",

        {

            "profile": profile,

        },

    )





@login_required
def delete_avatar(request):


    profile = get_object_or_404(

        UserProfile,

        user=request.user,

    )



    if profile.avatar:


        profile.avatar.delete(

            save=False

        )


        profile.avatar = None


        profile.save()



        create_activity_log(

            request.user,

            "avatar_delete",

            "تصویر پروفایل حذف شد.",

            request,

        )



        messages.success(

            request,

            "تصویر پروفایل حذف شد."

        )



    return redirect(

        "accounts:profile"

    )

@login_required
def dashboard(request):


    orders = Order.objects.filter(

        user=request.user

    ).select_related(

        "service",

    ).order_by(

        "-created_at",

    )



    notifications = request.user.notifications.filter(

        is_read=False,

    ).order_by(

        "-created_at",

    )[:5]



    profile = getattr(

        request.user,

        "profile",

        None,

    )



    context = {


        "orders": orders,


        "notifications": notifications,


        "profile": profile,


        "orders_count": orders.count(),



        "completed": orders.filter(

            status="completed",

        ).count(),



        "processing": orders.filter(

            status="processing",

        ).count(),



        "pending": orders.filter(

            status="pending",

        ).count(),



        "cancelled": orders.filter(

            status="cancelled",

        ).count(),



        "unread_notifications": notifications.count(),


    }



    return render(

        request,

        "accounts/dashboard.html",

        context,

    )





@login_required
def notifications_view(request):


    notifications = request.user.notifications.order_by(

        "-created_at"

    )



    notifications.update(

        is_read=True

    )



    return render(

        request,

        "accounts/notifications.html",

        {

            "notifications": notifications,

        },

    )





@login_required
def mark_notification_read(request, notification_id):


    notification = get_object_or_404(

        Notification,

        id=notification_id,

        user=request.user,

    )



    notification.is_read = True



    notification.save(

        update_fields=[

            "is_read",

        ]

    )



    return redirect(

        "accounts:notifications"

    )

@login_required
def my_orders(request):


    orders = Order.objects.filter(

        user=request.user,

    ).select_related(

        "service",

    ).order_by(

        "-created_at",

    )


    return render(

        request,

        "accounts/orders.html",

        {

            "orders": orders,

        },

    )





@login_required
def order_detail(request, tracking_code):


    order = get_object_or_404(

        Order,

        tracking_code=tracking_code,

        user=request.user,

    )



    tickets = order.tickets.all().order_by(

        "created_at",

    )



    progresses = order.progresses.all().order_by(

        "-created_at",

    )



    timeline = order.timeline.all().order_by(

        "created_at",

    )



    versions = order.versions.all().order_by(

        "-created_at",

    )



    invoice = getattr(

        order,

        "invoice",

        None,

    )



    context = {


        "order": order,


        "tickets": tickets,


        "progresses": progresses,


        "timeline": timeline,


        "versions": versions,


        "invoice": invoice,


    }



    return render(

        request,

        "accounts/order_detail.html",

        context,

    )





@login_required
def cancel_order(request, tracking_code):


    order = get_object_or_404(

        Order,

        tracking_code=tracking_code,

        user=request.user,

    )



    if order.status == "pending":


        order.status = "cancelled"



        order.save(

            update_fields=[

                "status",

            ]

        )



        create_activity_log(

            request.user,

            "order_cancel",

            f"لغو سفارش {tracking_code}",

            request,

        )



        create_notification(

            request.user,

            "لغو سفارش",

            "درخواست لغو سفارش ثبت شد.",

            "system",

        )



        messages.success(

            request,

            "درخواست لغو سفارش ثبت شد."

        )



    else:


        messages.error(

            request,

            "این سفارش قابل لغو نیست."

        )



    return redirect(

        "accounts:order_detail",

        tracking_code=tracking_code,

    )

@login_required
def create_ticket(request, tracking_code):


    order = get_object_or_404(

        Order,

        tracking_code=tracking_code,

        user=request.user,

    )



    if request.method == "POST":


        form = TicketForm(

            request.POST,

            request.FILES,

        )



        if form.is_valid():


            ticket = form.save(

                commit=False

            )


            ticket.order = order


            ticket.sender = request.user


            ticket.save()



            create_activity_log(

                request.user,

                "ticket_create",

                f"ایجاد تیکت برای سفارش {tracking_code}",

                request,

            )



            create_notification(

                request.user,

                "تیکت جدید",

                "تیکت شما با موفقیت ثبت شد.",

                "system",

            )



            messages.success(

                request,

                "تیکت با موفقیت ارسال شد."

            )



            return redirect(

                "accounts:order_detail",

                tracking_code=tracking_code,

            )



    else:


        form = TicketForm()



    return render(

        request,

        "accounts/create_ticket.html",

        {

            "form": form,

            "order": order,

        },

    )





@login_required
def ticket_list(request):


    tickets = Ticket.objects.filter(

        sender=request.user,

    ).select_related(

        "order",

    ).order_by(

        "-created_at",

    )



    return render(

        request,

        "accounts/tickets.html",

        {

            "tickets": tickets,

        },

    )





@login_required
def ticket_detail(request, ticket_id):


    ticket = get_object_or_404(

        Ticket,

        id=ticket_id,

        sender=request.user,

    )



    return render(

        request,

        "accounts/ticket_detail.html",

        {

            "ticket": ticket,

        },

    )





@login_required
def reply_ticket(request, ticket_id):


    ticket = get_object_or_404(

        Ticket,

        id=ticket_id,

        sender=request.user,

    )



    if request.method == "POST":


        form = TicketReplyForm(

            request.POST

        )



        if form.is_valid():


            reply = form.save(

                commit=False

            )


            reply.ticket = ticket


            reply.sender = request.user


            reply.save()



            create_activity_log(

                request.user,

                "ticket_reply",

                f"پاسخ به تیکت {ticket.id}",

                request,

            )



            create_notification(

                request.user,

                "پاسخ تیکت",

                "پاسخ شما به تیکت ثبت شد.",

                "system",

            )



            messages.success(

                request,

                "پاسخ شما ثبت شد."

            )



            return redirect(

                "accounts:ticket_detail",

                ticket_id=ticket.id,

            )


    else:


        form = TicketReplyForm()



    return render(

        request,

        "accounts/ticket_reply.html",

        {

            "form": form,

            "ticket": ticket,

        },

    )

@login_required
def invoice_detail(request, tracking_code):


    order = get_object_or_404(

        Order,

        tracking_code=tracking_code,

        user=request.user,

    )



    invoice = getattr(

        order,

        "invoice",

        None,

    )



    if invoice is None:


        messages.error(

            request,

            "فاکتوری برای این سفارش وجود ندارد."

        )


        return redirect(

            "accounts:order_detail",

            tracking_code=tracking_code,

        )



    return render(

        request,

        "accounts/invoice_detail.html",

        {

            "order": order,

            "invoice": invoice,

        },

    )





@login_required
def payment_history(request):


    invoices = Invoice.objects.filter(

        order__user=request.user,

    ).select_related(

        "order",

    ).order_by(

        "-created_at",

    )



    return render(

        request,

        "accounts/payment_history.html",

        {

            "invoices": invoices,

        },

    )





@login_required
def download_invoice(request, tracking_code):


    order = get_object_or_404(

        Order,

        tracking_code=tracking_code,

        user=request.user,

    )



    invoice = getattr(

        order,

        "invoice",

        None,

    )



    if invoice is None:


        return HttpResponse(

            "Invoice not found",

            status=404,

        )



    response = HttpResponse(

        content_type="application/pdf",

    )



    response["Content-Disposition"] = (

        f'attachment; filename="Nexora-{tracking_code}.pdf"'

    )



    pdf = canvas.Canvas(

        response

    )



    pdf.setTitle(

        f"Nexora Invoice {tracking_code}"

    )



    pdf.drawString(

        80,

        800,

        "NEXORA WEB INVOICE"

    )



    pdf.drawString(

        80,

        760,

        f"Tracking Code: {tracking_code}"

    )



    pdf.drawString(

        80,

        720,

        f"Service: {order.service}"

    )



    pdf.drawString(

        80,

        680,

        f"Amount: {invoice.amount:,} Toman"

    )



    pdf.drawString(

        80,

        640,

        f"Status: {invoice.get_status_display()}"

    )



    pdf.save()



    create_activity_log(

        request.user,

        "invoice_download",

        f"دانلود فاکتور {tracking_code}",

        request,

    )



    create_notification(

        request.user,

        "دانلود فاکتور",

        "فاکتور سفارش شما دانلود شد.",

        "system",

    )



    return response

@login_required
def activity_history(request):


    activities = UserActivityLog.objects.filter(

        user=request.user,

    ).order_by(

        "-created_at",

    )



    return render(

        request,

        "accounts/activity_history.html",

        {

            "activities": activities,

        },

    )





@login_required
def security_center(request):


    activities = UserActivityLog.objects.filter(

        user=request.user,

    ).order_by(

        "-created_at",

    )[:20]



    profile = getattr(

        request.user,

        "profile",

        None,

    )



    context = {


        "activities": activities,


        "profile": profile,


        "last_login": request.user.last_login,


        "date_joined": request.user.date_joined,


    }



    return render(

        request,

        "accounts/security.html",

        context,

    )





@login_required
def account_settings(request):


    profile, created = UserProfile.objects.get_or_create(

        user=request.user,

    )



    return render(

        request,

        "accounts/settings.html",

        {

            "profile": profile,

        },

    )





@login_required
def check_user_role(request):


    profile = getattr(

        request.user,

        "profile",

        None,

    )



    if not profile:


        raise PermissionDenied



    return render(

        request,

        "accounts/role.html",

        {

            "role": profile.role,

        },

    )





def permission_denied_view(request):


    messages.error(

        request,

        "شما اجازه دسترسی به این بخش را ندارید."

    )


    return redirect(

        "accounts:dashboard"

    )

def accounts_context(request):


    if not request.user.is_authenticated:

        return {}



    unread_notifications = Notification.objects.filter(

        user=request.user,

        is_read=False,

    ).count()



    return {

        "current_user": request.user,

        "unread_notifications": unread_notifications,

    }





@login_required
def mark_all_notifications_read(request):


    Notification.objects.filter(

        user=request.user,

        is_read=False,

    ).update(

        is_read=True

    )



    create_activity_log(

        request.user,

        "notifications_read",

        "تمام اعلان‌ها خوانده شدند.",

        request,

    )



    return redirect(

        "accounts:notifications"

    )





def account_error(request):


    messages.error(

        request,

        "خطایی در حساب کاربری رخ داد."

    )


    return redirect(

        "accounts:dashboard"

    )





def account_not_found(request):


    messages.error(

        request,

        "اطلاعات مورد نظر پیدا نشد."

    )


    return redirect(

        "core:home"

    )





@login_required
def refresh_dashboard_data(request):


    orders_count = Order.objects.filter(

        user=request.user,

    ).count()



    notifications_count = Notification.objects.filter(

        user=request.user,

        is_read=False,

    ).count()



    return render(

        request,

        "accounts/dashboard_refresh.html",

        {

            "orders_count": orders_count,

            "notifications_count": notifications_count,

        },

    )

__all__ = [

    "register_view",

    "login_view",

    "logout_view",


    "verify_email",

    "resend_email_verification",


    "password_reset_request",

    "password_reset_complete",

    "change_password",


    "profile_view",

    "profile_detail",

    "delete_avatar",


    "dashboard",

    "notifications_view",

    "mark_notification_read",

    "mark_all_notifications_read",


    "my_orders",

    "order_detail",

    "cancel_order",


    "create_ticket",

    "ticket_list",

    "ticket_detail",

    "reply_ticket",


    "invoice_detail",

    "payment_history",

    "download_invoice",


    "activity_history",

    "security_center",

    "account_settings",


    "accounts_context",

]
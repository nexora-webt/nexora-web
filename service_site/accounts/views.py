from django.contrib import messages
from django.contrib.auth import (login,logout,update_session_auth_hash,)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
from core.models import Order
from .forms import RegisterForm, ProfileForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)

    if form.is_valid():

        user = form.save()

        user.email = form.cleaned_data["email"]

        user.save()

        login(request, user)

        messages.success(
            request,
            "ثبت نام با موفقیت انجام شد."
        )

        return redirect("dashboard")

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = AuthenticationForm(
        request,
        data=request.POST or None,
    )

    if form.is_valid():

        login(
            request,
            form.get_user(),
        )

        return redirect("dashboard")

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def dashboard(request):

    orders = Order.objects.filter(
        user=request.user
    ).select_related(
        "service",
    ).order_by(
        "-created_at"
    )

    notifications = request.user.notifications.all()[:5]

    is_manager = request.user.role == "manager"

    context = {

        "is_manager": is_manager,

        "orders": orders,

        "notifications": notifications,

        "orders_count": orders.count(),

        "completed": orders.filter(
            status="completed"
        ).count(),

        "processing": orders.filter(
            status="processing"
        ).count(),

        "pending": orders.filter(
            status="pending"
        ).count(),

    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )


@login_required
def profile_view(request):

    profile = request.user.profile

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "پروفایل بروزرسانی شد."
        )

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
        },
    )

@login_required
def change_password(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "رمز عبور با موفقیت تغییر کرد."
            )

            return redirect("profile")

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form,
        },
    )
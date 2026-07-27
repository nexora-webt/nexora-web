from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def get_user_role(user):

    if not user.is_authenticated:
        return None

    try:
        return user.profile.role

    except Exception:
        return "client"



def role_required(allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            role = get_user_role(request.user)

            if role not in allowed_roles:

                messages.error(
                    request,
                    "شما دسترسی لازم برای این بخش را ندارید."
                )

                return redirect("core:home")

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator



def client_required(view_func):

    return role_required(
        ["client"]
    )(view_func)



def manager_required(view_func):

    return role_required(
        [
            "manager",
            "admin",
        ]
    )(view_func)



def developer_required(view_func):

    return role_required(
        [
            "developer",
            "manager",
            "admin",
        ]
    )(view_func)

def staff_required(view_func):

    return role_required(
        [
            "developer",
            "manager",
        ]
    )(view_func)



def admin_or_manager_required(view_func):

    return role_required(
        [
            "manager",
            "admin",
        ]
    )(view_func)

def can_access_order(user, order):

    role = get_user_role(user)


    if role == "admin":

        return True


    if role == "manager":

        return True


    if role == "developer":

        return order.developers.filter(
            id=user.id
        ).exists()


    if role == "client":

        return order.user == user


    return False
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_verification_email(request, user):

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )


    token = default_token_generator.make_token(
        user
    )


    verification_url = request.build_absolute_uri(

        reverse(
            "accounts:verify_email",
            kwargs={
                "uidb64": uid,
                "token": token,
            },
        )

    )


    message = f"""
سلام {user.username}

برای فعال سازی حساب Nexora Web روی لینک زیر کلیک کنید:

{verification_url}

اگر شما این درخواست را انجام نداده‌اید، این ایمیل را نادیده بگیرید.
"""


    send_mail(

        subject="تایید حساب Nexora Web",

        message=message,

        from_email=None,

        recipient_list=[
            user.email
        ],

    )
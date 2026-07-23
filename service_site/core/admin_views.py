from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect


@staff_member_required(login_url="/login/")
def secure_admin(request):
    return site.index(request)
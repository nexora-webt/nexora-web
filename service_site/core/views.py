# ==========================================================
# IMPORTS
# ==========================================================

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from .forms import JobApplicationForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.http import HttpResponse

from django_ratelimit.decorators import ratelimit

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


from .models import (
    Service,
    Portfolio,
    Order,
    ContactMessage,
    Invoice,
)


from .forms import (
    OrderForm,
    ContactForm,
)



# ==========================================================
# AI PRICE CALCULATOR
# ==========================================================

def calculate_price(service, description):

    base = service.base_price

    desc = description.lower()

    complexity = 1

    time_estimate = "۷ تا ۱۰ روز کاری"



    # ======================================================
    # WEBSITE COMPLEXITY
    # ======================================================

    if any(
        word in desc
        for word in [
            "فروشگاه",
            "فروشگاهی",
            "shop",
            "ecommerce",
        ]
    ):

        complexity += 1.8

        time_estimate = "۱۴ تا ۲۵ روز کاری"



    elif any(
        word in desc
        for word in [
            "رزومه",
            "شخصی",
            "لندینگ",
            "portfolio",
        ]
    ):

        complexity += 0.5

        time_estimate = "۵ تا ۸ روز کاری"



    elif any(
        word in desc
        for word in [
            "اپلیکیشن",
            "اپ",
            "mobile",
        ]
    ):

        complexity += 2.5

        time_estimate = "۲۵ تا ۴۵ روز کاری"



    # ======================================================
    # EXTRA FEATURES
    # ======================================================

    if any(
        word in desc
        for word in [
            "ai",
            "هوش مصنوعی",
            "انیمیشن",
            "سه بعدی",
            "3d",
        ]
    ):

        complexity += 1.2



    length_factor = len(description) / 200



    final_price = int(
        base
        * complexity
        * (1 + length_factor)
    )


    final_price = max(
        final_price,
        base,
    )


    return final_price, time_estimate

# ==========================================================
# HOME
# ==========================================================

@ratelimit(
    key="ip",
    rate="5/m",
    method="POST",
    block=True,
)
def home(request):

    services = Service.objects.filter(
        is_active=True
    )

    portfolios = Portfolio.objects.filter(
        is_active=True
    ).order_by(
        "-created_at"
    )[:6]


    order_form = OrderForm()

    contact_form = ContactForm()



    # ======================================================
    # ORDER SUBMIT
    # ======================================================

    if request.method == "POST" and "order_submit" in request.POST:


        order_form = OrderForm(
            request.POST,
            request.FILES,
        )


        if order_form.is_valid():

            with transaction.atomic():

                order = order_form.save(
                    commit=False
                )


                if request.user.is_authenticated:

                    order.user = request.user



                price, time_estimate = calculate_price(
                    order.service,
                    order.description,
                )


                order.estimated_price = price


                order.save()



                messages.success(
                    request,
                    f"""
                    سفارش شما با موفقیت ثبت شد.

                    کد پیگیری:
                    {order.tracking_code}

                    هزینه تقریبی:
                    {price:,} تومان

                    زمان انجام:
                    {time_estimate}
                    """
                )


                return redirect(
                    "core:success"
                )



    # ======================================================
    # CONTACT SUBMIT
    # ======================================================

    elif request.method == "POST" and "contact_submit" in request.POST:


        contact_form = ContactForm(
            request.POST
        )


        if contact_form.is_valid():

            contact_form.save()


            messages.success(
                request,
                "پیام شما با موفقیت ارسال شد."
            )


            return redirect(
                "core:home"
            )



    context = {

        "services": services,

        "portfolios": portfolios,

        "order_form": order_form,

        "contact_form": contact_form,

    }



    return render(
        request,
        "home.html",
        context,
    )

# ==========================================================
# SERVICE DETAIL
# ==========================================================

def service_detail(request, slug):

    service = get_object_or_404(
        Service,
        slug=slug,
        is_active=True,
    )


    related_projects = Portfolio.objects.filter(
        category=service.category,
        is_active=True,
    ).order_by(
        "-created_at"
    )[:6]


    context = {

        "service": service,

        "related_projects": related_projects,

    }

    context["services"] = Service.objects.all()

    return render(
        request,
        "service_detail.html",
        context,
    )



# ==========================================================
# PORTFOLIO DETAIL
# ==========================================================

def portfolio_detail(request, slug):

    project = get_object_or_404(
        Portfolio,
        slug=slug,
        is_active=True,
    )


    images = project.images.all().order_by(
        "order"
    )


    related_projects = Portfolio.objects.filter(
        category=project.category,
        is_active=True,
    ).exclude(
        id=project.id,
    ).order_by(
        "-created_at"
    )[:3]



    context = {

        "project": project,

        "images": images,

        "related_projects": related_projects,

    }



    return render(
        request,
        "portfolio_detail.html",
        context,
    )

# ==========================================================
# CONTACT
# ==========================================================

@ratelimit(
    key="ip",
    rate="5/m",
    method="POST",
    block=True,
)
def contact(request):

    form = ContactForm()


    if request.method == "POST":

        form = ContactForm(
            request.POST
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "پیام شما با موفقیت ثبت شد."
            )


            return redirect(
                "core:contact"
            )


    return render(
        request,
        "contact.html",
        {
            "form": form,
        },
    )



# ==========================================================
# ABOUT
# ==========================================================

def about(request):

    return render(
        request,
        "about.html",
    )



# ==========================================================
# SUCCESS
# ==========================================================

def success(request):

    return render(
        request,
        "success.html",
    )

# ==========================================================
# ORDER TRACKING
# ==========================================================

def tracking(request):

    order = None

    code = request.GET.get(
        "code"
    )


    if code:

        try:

            order = Order.objects.select_related(
                "service",
            ).get(
                tracking_code=code,
            )


        except Order.DoesNotExist:

            messages.error(
                request,
                "سفارشی با این کد پیگیری پیدا نشد."
            )



    return render(
        request,
        "tracking.html",
        {
            "order": order,
            "tracking_code": code,
        },
    )

# ==========================================================
# USER DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    orders = Order.objects.filter(
        user=request.user,
    ).select_related(
        "service",
    ).order_by(
        "-created_at",
    )


    context = {

        "orders": orders,

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

    }


    return render(
        request,
        "dashboard.html",
        context,
    )

# ==========================================================
# ORDER DETAIL
# ==========================================================

@login_required
def order_detail(request, tracking_code):

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


    files = order.files.all()


    payments = order.payments.all().order_by(
        "-created_at",
    )


    context = {

        "order": order,

        "files": files,

        "payments": payments,

        "invoice": invoice,

    }


    return render(
        request,
        "order_detail.html",
        context,
    )

# ==========================================================
# INVOICE PDF
# ==========================================================

@login_required
def invoice_pdf(request, tracking_code):

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
        f'attachment; filename="invoice-{tracking_code}.pdf"'
    )


    pdf = canvas.Canvas(
        response,
    )


    pdf.setTitle(
        f"Invoice {tracking_code}",
    )


    # ======================================================
    # HEADER
    # ======================================================

    pdf.setFont(
        "Helvetica-Bold",
        18,
    )


    pdf.drawString(
        2 * cm,
        27 * cm,
        "NEXORA WEB",
    )


    pdf.setFont(
        "Helvetica",
        11,
    )


    pdf.drawString(
        2 * cm,
        26.2 * cm,
        "Professional Web Solutions",
    )


    pdf.line(
        2 * cm,
        25.8 * cm,
        19 * cm,
        25.8 * cm,
    )


    # ======================================================
    # INVOICE INFO
    # ======================================================

    pdf.drawString(
        2 * cm,
        25 * cm,
        f"Invoice: {invoice.invoice_number}",
    )


    pdf.drawString(
        2 * cm,
        24 * cm,
        f"Tracking Code: {tracking_code}",
    )


    pdf.drawString(
        2 * cm,
        23 * cm,
        f"Customer: {request.user.username}",
    )


    pdf.drawString(
        2 * cm,
        22 * cm,
        f"Service: {order.service.title}",
    )


    pdf.drawString(
        2 * cm,
        21 * cm,
        f"Amount: {invoice.amount:,} Toman",
    )


    pdf.drawString(
        2 * cm,
        20 * cm,
        f"Status: {invoice.get_status_display()}",
    )


    # ======================================================
    # FOOTER
    # ======================================================

    pdf.line(
        2 * cm,
        3 * cm,
        19 * cm,
        3 * cm,
    )


    pdf.drawString(
        2 * cm,
        2.3 * cm,
        "Thank you for choosing Nexora Web.",
    )


    pdf.save()


    return response

# ==========================================================
# WEBSITE CONTEXT
# ==========================================================

def website_context():

    return {

        "company_name": "Nexora Web",

        "holding": "Nexora Holding",

        "website": "https://nexora.ir",

        "email": "info@nexora.ir",

        "phone": "+98 933 061 6352",

    }



# ==========================================================
# ERROR HANDLERS
# ==========================================================

def error_400(request, exception):

    return render(
        request,
        "400.html",
        {
            "status_code": 400,
            **website_context(),
        },
        status=400,
    )



def error_403(request, exception):

    return render(
        request,
        "403.html",
        {
            "status_code": 403,
            **website_context(),
        },
        status=403,
    )



def error_404(request, exception):

    return render(
        request,
        "404.html",
        {
            "status_code": 404,
            **website_context(),
        },
        status=404,
    )



def error_500(request):

    return render(
        request,
        "500.html",
        {
            "status_code": 500,
            **website_context(),
        },
        status=500,
    )

def careers(request):
    return render(
        request,
        "careers.html"
    )

def careers(request):

    form = JobApplicationForm()

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save()

            messages.success(
                request,
                "درخواست همکاری شما با موفقیت ثبت شد."
            )

            return redirect("core:careers")


    return render(
        request,
        "careers.html",
        {
            "form": form
        }
    )

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.http import HttpResponse


from .models import (
    Service,
    Portfolio,
    Order,
)


from .forms import (
    OrderForm,
    ContactForm,
)
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from .models import (
    Service,
    Portfolio,
    Career,
    Order,
    Ticket,
)

from .forms import (
    OrderForm,
    ContactForm,
    JobApplicationForm,
    TicketForm,
)

# ==========================================================
# AI PRICE CALCULATOR
# ==========================================================

def calculate_price(service, description):
    """
    AI Price Calculator
    """

    base = service.base_price

    desc = description.lower()

    complexity = 1.0

    time_estimate = "۷-۱۰ روز کاری"

    # ==========================================
    # Website Types
    # ==========================================

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

        time_estimate = "۱۴-۲۵ روز"

    elif any(

        word in desc

        for word in [

            "رزومه",

            "شخصی",

            "لندینگ",

            "پورتفولیو",

        ]

    ):

        complexity += 0.5

        time_estimate = "۵-۸ روز"

    elif any(

        word in desc

        for word in [

            "اپ",

            "موبایل",

        ]

    ):

        complexity += 2.3

        time_estimate = "۲۵-۴۰ روز"

    # ==========================================
    # Animation
    # ==========================================

    if any(

        word in desc

        for word in [

            "انیمیشن",

            "سینمایی",

            "خفن",

            "immersive",

        ]

    ):

        complexity += 1.1

    length_factor = len(description) / 180

    final_price = int(

        base * complexity * (1 + length_factor)

    )

    final_price = max(

        final_price,

        base,

    )

    return final_price, time_estimate

# ==========================================================
# HOME
# ==========================================================

def home(request):

    services = Service.objects.all()

    portfolios = Portfolio.objects.order_by(

        "-created_at"

    )[:6]

    form = OrderForm()

    contact_form = ContactForm()

    # ==========================================
    # ORDER FORM
    # ==========================================

    if request.method == "POST" and "order_submit" in request.POST:

        form = OrderForm(

            request.POST,

            request.FILES,

        )

        if form.is_valid():

            with transaction.atomic():

                order = form.save(

                    commit=False,

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

                    🎉 سفارش شما با موفقیت ثبت شد.

                    کد پیگیری:

                    {order.tracking_code}

                    هزینه تقریبی:

                    {price:,} تومان

                    زمان تقریبی انجام:

                    {time_estimate}

                    """,

                )

                return redirect(
                    "core:success",
                )

    # ==========================================
    # CONTACT FORM
    # ==========================================

    elif request.method == "POST" and "contact_submit" in request.POST:

        contact_form = ContactForm(

            request.POST,

        )

        if contact_form.is_valid():

            contact_form.save()

            messages.success(

                request,

                "پیام شما با موفقیت ارسال شد.",

            )

            return redirect(
                "core:home",
            )

    context = {

        "services": services,

        "portfolios": portfolios,

        "form": form,

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

    )

    portfolios = Portfolio.objects.filter(

        service=service,

    ).order_by(

        "-created_at",

    )

    context = {

        "service": service,

        "portfolios": portfolios,

    }

    return render(

        request,

        "service_detail.html",

        context,

    )


# ==========================================================
# CONTACT
# ==========================================================

def contact(request):

    form = ContactForm()

    if request.method == "POST":

        form = ContactForm(

            request.POST,

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "پیام شما با موفقیت ثبت شد.",

            )

            return redirect(

                "contact",

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
# CAREERS
# ==========================================================

def careers(request):

    jobs = Career.objects.filter(

        active=True,

    ).order_by(

        "-created_at",

    )

    form = JobApplicationForm()

    if request.method == "POST":

        form = JobApplicationForm(

            request.POST,

            request.FILES,

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "رزومه شما با موفقیت ثبت شد.",

            )

            return redirect(

                "careers",

            )

    context = {

        "jobs": jobs,

        "form": form,

    }

    return render(

        request,

        "careers.html",

        context,

    )


# ==========================================================
# PORTFOLIO DETAIL
# ==========================================================

def portfolio_detail(request, slug):

    project = get_object_or_404(

        Portfolio,

        slug=slug,

    )

    related_projects = Portfolio.objects.filter(

        service=project.service,

    ).exclude(

        id=project.id,

    ).order_by(

        "-created_at",

    )[:3]

    context = {

        "project": project,

        "related_projects": related_projects,

    }

    return render(

        request,

        "portfolio_detail.html",

        context,

    )

# ==========================================================
# TRACKING
# ==========================================================

def tracking(request):

    order = None

    code = request.GET.get("code")

    if code:

        try:

            order = Order.objects.select_related(

                "service",

            ).get(

                tracking_code=code,

            )

        except Order.DoesNotExist:

            order = None

            messages.error(

                request,

                "سفارشی با این کد پیگیری پیدا نشد.",

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
# DASHBOARD
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

    tickets = order.tickets.all().order_by(

        "created_at",

    )

    progresses = order.progresses.all().order_by(

        "created_at",

    )

    timeline = order.timeline.all().order_by(

        "created_at",

    )

    versions = order.versions.all().order_by(

        "-created_at",

    )

    tasks = order.tasks.all().order_by(

        "created_at",

    )

    invoice = getattr(

        order,

        "invoice",

        None,

    )

    form = TicketForm(

        request.POST or None,

        request.FILES or None,

    )

    # ==========================================
    # NEW TICKET
    # ==========================================

    if request.method == "POST":

        if form.is_valid():

            ticket = form.save(

                commit=False,

            )

            ticket.order = order

            ticket.sender = request.user

            ticket.save()

            messages.success(

                request,

                "تیکت شما با موفقیت ارسال شد.",

            )

            return redirect(

                "order_detail",

                tracking_code=tracking_code,

            )

    context = {

        "order": order,

        "tickets": tickets,

        "versions": versions,

        "timeline": timeline,

        "tasks": tasks,

        "progresses": progresses,

        "invoice": invoice,

        "form": form,

    }

    return render(

        request,

        "accounts/order_detail.html",

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

        f'attachment; filename="Invoice-{tracking_code}.pdf"'

    )

    pdf = canvas.Canvas(

        response,

    )

    pdf.setTitle(

        f"Invoice {tracking_code}",

    )

    # ==========================================
    # Header
    # ==========================================

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

        "Professional Website Design",

    )

    pdf.line(

        2 * cm,

        25.8 * cm,

        19 * cm,

        25.8 * cm,

    )

    # ==========================================
    # Invoice Information
    # ==========================================

    pdf.drawString(

        2 * cm,

        25 * cm,

        f"Tracking Code : {tracking_code}",

    )

    pdf.drawString(

        2 * cm,

        24 * cm,

        f"Customer : {request.user.get_full_name() or request.user.username}",

    )

    pdf.drawString(

        2 * cm,

        23 * cm,

        f"Service : {order.service}",

    )

    pdf.drawString(

        2 * cm,

        22 * cm,

        f"Amount : {invoice.amount:,} Toman",

    )

    pdf.drawString(

        2 * cm,

        21 * cm,

        f"Status : {invoice.get_status_display()}",

    )

    pdf.drawString(

        2 * cm,

        20 * cm,

        f"Due Date : {invoice.due_date}",

    )

    # ==========================================
    # Footer
    # ==========================================

    pdf.line(

        2 * cm,

        3.2 * cm,

        19 * cm,

        3.2 * cm,

    )

    pdf.drawString(

        2 * cm,

        2.5 * cm,

        "Thank you for choosing Nexora Web.",

    )

    pdf.drawString(

        2 * cm,

        1.8 * cm,

        "https://nexora.ir",

    )

    pdf.save()

    return response

# ==========================================================
# COMMON CONTEXT HELPERS
# ==========================================================

def website_context():

    return {

        "company_name": "Nexora Web",

        "holding": "Nexora Holding",

        "website": "https://nexora.ir",

        "email": "info@nexora.ir",

        "phone": "+98 900 000 0000",

    }


# ==========================================================
# CUSTOM ERROR PAGES
# ==========================================================

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


# ==========================================================
# FILE END
# ==========================================================
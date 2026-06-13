from django.shortcuts import render, redirect
from .models import Service, Portfolio
from .forms import OrderForm

def calculate_price(service, description):
    """هوش مصنوعی قیمت‌گذاری واقعی"""
    base = service.base_price
    desc = description.lower()
    complexity = 1.0
    time_estimate = "۷-۱۰ روز کاری"

    if any(word in desc for word in ['فروشگاه', 'فروشگاهی', 'shop', 'ecommerce']):
        complexity += 1.8
        time_estimate = "۱۴-۲۵ روز"
    elif any(word in desc for word in ['رزومه', 'شخصی', 'لندینگ', 'پورتفولیو']):
        complexity += 0.5
        time_estimate = "۵-۸ روز"
    elif any(word in desc for word in ['اپ', 'موبایل']):
        complexity += 2.3
        time_estimate = "۲۵-۴۰ روز"

    if any(word in desc for word in ['انیمیشن', 'سینمایی', 'خفن', 'immersive']):
        complexity += 1.1

    length_factor = len(description) / 180
    final_price = int(base * complexity * (1 + length_factor))
    final_price = max(final_price, base)

    return final_price, time_estimate

def home(request):
    services = Service.objects.all()
    portfolios = Portfolio.objects.all()[:6]  # فقط ۶ تا نشون بده
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.estimated_price, _ = calculate_price(order.service, order.description)
            order.save()
            return redirect('success')

    context = {
        'services': services,
        'portfolios': portfolios,
        'form': form,
    }
    return render(request, 'home.html', context)

def success(request):
    return render(request, 'success.html')
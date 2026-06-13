from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=150, verbose_name="نام خدمت")
    description = models.TextField(verbose_name="توضیحات")
    base_price = models.IntegerField(verbose_name="قیمت پایه (تومان)")
    icon = models.CharField(max_length=100, blank=True, verbose_name="آیکون Font Awesome")
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    def str(self):
        return self.title

class Portfolio(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان پروژه")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image = models.ImageField(upload_to='portfolio/', verbose_name="عکس نمونه کار")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='projects')
    link = models.URLField(blank=True, verbose_name="لینک پروژه")
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title

    class Meta:
        verbose_name = "نمونه کار"
        verbose_name_plural = "نمونه کارها"
        
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار بررسی'),
        ('processing', 'در حال انجام'),
        ('completed', 'تحویل داده شد'),
    ]
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="نوع خدمت")
    description = models.TextField(verbose_name="توضیحات پروژه")
    estimated_price = models.IntegerField(verbose_name="قیمت تخمینی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"سفارش {self.name} - {self.service.title}"
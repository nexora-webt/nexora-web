from .models import Service


def global_data(request):
    return {
        "global_services": Service.objects.all(),
    }
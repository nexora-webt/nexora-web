from .models import Service

def global_data(request):

    return {

        "services_menu": Service.objects.filter(active=True),

    }
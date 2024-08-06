from django.shortcuts import get_object_or_404, render

from service.models import Service


def service_list(request):
    services = Service.published_objects.all()

    return render(
        request,
        'service/index.html',
        context={'services': services}
    )


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, status=Service.Status.PUBLISHED)

    return render(
        request,
        'service/detail.html',
        context={'service': service}
    )



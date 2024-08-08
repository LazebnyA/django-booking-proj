from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

from service.models import Service


def service_list(request):
    services = Service.published_objects.all()

    paginator = Paginator(services, 9)
    page_number = request.GET.get('page', 1)

    try:
        services = paginator.page(page_number)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)

    return render(
        request,
        'service/index.html',
        context={'services': services}
    )


def service_detail(request, year, month, day, service_slug):
    service = get_object_or_404(
        Service,
        status=Service.Status.PUBLISHED,
        slug=service_slug,
        published__year=year,
        published__month=month,
        published__day=day,
    )

    return render(
        request,
        'service/detail.html',
        context={'service': service}
    )



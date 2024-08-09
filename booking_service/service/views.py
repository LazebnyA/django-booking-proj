from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from service.forms import ShareServiceForm
from service.models import Service


# Class-based view

class ServiceList(ListView):
    """
    Class-based view for listing all services available for booking.
    """
    queryset = Service.objects.all()
    context_object_name = 'services'
    paginate_by = 9
    template_name = "service/index.html"


# def service_list(request):
#     services = Service.published_objects.all()
#
#     paginator = Paginator(services, 9)
#     page_number = request.GET.get('page', 1)
#
#     try:
#         services = paginator.page(page_number)
#     except PageNotAnInteger:
#         services = paginator.page(1)
#     except EmptyPage:
#         services = paginator.page(paginator.num_pages)
#
#     return render(
#         request,
#         'service/index.html',
#         context={'services': services}
#     )


def service_detail(request, year, month, day, service_slug):
    """
    View for showing details of a single service.
    """
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


def service_share(request, service_id):
    service = get_object_or_404(
        Service,
        status=Service.Status.PUBLISHED,
        pk=service_id,
    )

    sent = False

    if request.method == "POST":
        form = ShareServiceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            service_url = request.build_absolute_uri(service.get_absolute_url())
            subject = (
                f"{cd['name']} {cd['email']} "
                f"recommends you this service: {service.service_name}"
            )
            message = (
                f"Look at {service.service_name} at {service_url}\n\n"
                f"{cd['name']}'s comments: \n{cd['comments']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )

            sent = True
    else:
        form = ShareServiceForm()

    return render(request, 'service/share.html', context={'service': service, 'form': form, 'sent': sent})

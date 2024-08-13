from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from service.forms import ShareServiceForm, ServiceCommentForm, CreateServiceForm
from service.models import Service, ServiceComment
from user.models import User


# Class-based view

# class ServiceList(ListView):
#     """
#     Class-based view for listing all services available for booking.
#     """
#     queryset = Service.objects.all()
#     context_object_name = 'services'
#     paginate_by = 9
#     template_name = "service/index.html"


def service_list(request):
    services = Service.published_objects.all()

    tag_slug = request.GET.get('tag')
    search_q = request.GET.get('q')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        services = services.filter(tags__slug=tag.slug)
    elif search_q:
        search_vector = SearchVector(
            'service_name', weight='A', config='english'
        ) + SearchVector('description', weight='B', config='english')

        search_query = SearchQuery(search_q, search_type='plain')
        services = services.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
        ).filter(rank__gte=0.3).order_by('-rank')

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

    comments = service.comments.filter(active=True)

    service_tags_ids = service.tags.values_list('id', flat=True)
    similar_services = Service.published_objects.filter(
        tags__in=service_tags_ids
    ).exclude(id=service.id)
    similar_services = similar_services.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-published')[:4]

    return render(
        request,
        'service/detail.html',
        context={'service': service, 'comments': comments, 'similar_services': similar_services},
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


@require_POST
def service_comment(request, service_id):
    service = get_object_or_404(
        Service,
        status=Service.Status.PUBLISHED,
        pk=service_id,
    )

    form = ServiceCommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.service = service
        comment.save()

    return HttpResponseRedirect(service.get_absolute_url())


@login_required
def service_create(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = CreateServiceForm(data=request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.author = user
            service.save()

            messages.success(request, f'Service {request.POST['service_name']} created. Wait until administration '
                                      f'will publish it.')
            return HttpResponseRedirect(reverse('user:dashboard'))
        else:
            print(form.errors)
    else:
        form = CreateServiceForm()

    return render(request, 'service/create.html', context={'form': form})

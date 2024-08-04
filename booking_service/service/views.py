from django.shortcuts import render


def index(request):
    context = {
        'title': 'Service Marketplace',
        'content': 'Content',
    }

    return render(request, 'service/index.html', context)

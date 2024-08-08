from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from feedback.forms import FeedbackForm


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your feedback has been recorded!')
            return HttpResponseRedirect(reverse('feedback:feedback'))
    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback.html", {"form": form})

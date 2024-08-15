from django import forms

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    text = forms.CharField()

    class Meta:
        model = Feedback
        fields = ('text',)




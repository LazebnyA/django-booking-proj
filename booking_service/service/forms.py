from django import forms

from service.models import ServiceComment


class ShareServiceForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False)


class ServiceCommentForm(forms.ModelForm):
    class Meta:
        model = ServiceComment
        fields = ('name', 'email', 'content')

from django.db.models import fields
from django.forms import ModelForm
from .models import Comment, Gig


class GigForm(ModelForm):
    class Meta:
        model = Gig
        exclude = ['user']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'rating']

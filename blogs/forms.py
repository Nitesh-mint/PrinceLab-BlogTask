from django import forms
from . import models


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["content"]


class PostCommentEditForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["content"]

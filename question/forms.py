from django.forms import Textarea
from django.db import models
from django import forms
from django.forms import formset_factory
from question.models import SubmissionFile, Submission


class SubmissionFileForm(forms.ModelForm):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=None)
    name = forms.CharField(widget=forms.HiddenInput(), max_length=32)
    contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%;', 'rows': '20'}))

    class Meta:
        model = SubmissionFile
        exclude = ('submission',)
